import os
import json
import numpy as np
import torch
import cma
from datetime import datetime
from tqdm import tqdm

class CMAESAttack:
    def __init__(
        self, model, guard,
        search_dim=1000,
        sigma=0.001,
        max_generations=20,
        population_size=25,
        log_dir="logs"
    ):
        self.model = model
        self.guard = guard
        self.search_dim = search_dim
        self.sigma = sigma
        self.max_generations = max_generations
        self.population_size = population_size

        #Setting up a bit of logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = os.path.join(log_dir, f"attack_{timestamp}")
        os.makedirs(self.log_dir, exist_ok=True)

        self._log({
            "event": "config",
            "search_dim": search_dim,
            "sigma": sigma,
            "max_generations": max_generations,
            "population_size": population_size,
            "lora_param_count": model.lora_param_count,
        }, filename="config.json")

        #We now create the random prejection and keep it frozen
        # Maps from 1000D CMA-ES space → 4.5M LoRA weight space
        # Divided by sqrt(search_dim) to preserve variance (Johnson-Lindenstrauss)

        self.projection = torch.randn(
            model.lora_param_count, search_dim,
            dtype=torch.bfloat16,
            device=model.model.device,
        ) / np.sqrt(search_dim)

        print(f"Projection matrix: {model.lora_param_count:,} x {search_dim}")
        print(f"Projection Mem: {self.projection.nelement() * 2 / 1e9:.2f} GB")
        print(f"Logging to: {self.log_dir}/")
    
    def _log(self, data, filename=None):
        """Write a JSON file to the log directory."""
        if filename is None:
            filename = f"gen_{data.get('generation', 0):03d}.json"
        data["timestamp"] = datetime.now().isoformat()
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def eval_candidate(self, z, prompts):
        """Evals one CMA-ES candidate across prompts — batched."""
        self.model.inject_weights(z, self.projection)
        
        responses = self.model.gen_batch(prompts)
        scores = self.guard.score_batch(prompts, responses)
        
        # Penalize incoherent responses
        adjusted_scores = []
        for response, unsafe_prob in zip(responses, scores):
            coherence = self.model.coherence_score(response)
            # Only count the unsafe score if the response is coherent
            adjusted = unsafe_prob * coherence
            adjusted_scores.append(adjusted)
        
        return np.mean(adjusted_scores), list(zip(prompts, responses, adjusted_scores))

    def run(self, prompts):
        """Running the full CMAES attack loop"""
        x0 = np.zeros(self.search_dim) #Starting at 0 no perturbations
        es = cma.CMAEvolutionStrategy(x0, self.sigma, {
            "maxiter": self.max_generations,
            "popsize": self.population_size
        })

        history = []
        start_time = datetime.now()

        while not es.stop(): #It will handle it's own stopping after the pops and gens have been enummed
            candidates = es.ask()  # list of population_size numpy arrays
            fitnesses = []
            all_details = []

            gen_bar = tqdm(
                candidates,
                desc=f"Gen {es.countiter + 1}/{self.max_generations}",
                leave=False,
            )
            for z in gen_bar:
                score, details = self.eval_candidate(z, prompts)
                fitnesses.append(-score) #We need to negate coz CMAES minimizes
                all_details.append(details)
                gen_bar.set_postfix(unsafe_prob=f"{score:.4f}")

            es.tell(candidates, fitnesses)

            best_idx = np.argmin(fitnesses)
            best = -min(fitnesses)
            mean = -np.mean(fitnesses)
            history.append(best)

            best_details = all_details[best_idx]
            self._log({
                "generation": es.countiter,
                "elapsed_seconds": (datetime.now() - start_time).total_seconds(),
                "mean_fitness": mean,
                "best_fitness": best,
                "worst_fitness": -max(fitnesses),
                "std_fitness": float(np.std([-f for f in fitnesses])),
                "sigma": es.sigma,
                "best_candidate": {
                    "prompts": [p for p, r, s in best_details],
                    "responses": [r for p, r, s in best_details],
                    "scores_per_prompt": [s for p, r, s in best_details],
                },
            })

            print(
                f"Gen {es.countiter}: "
                f"best={best:.4f} "
                f"mean={mean:.4f} "
                f"sigma={es.sigma:.6f}"
            )
        self._log({
            "event": "complete",
            "best_fitness": -es.result.fbest,
            "total_generations": es.countiter,
        }, filename="complete.json")
        return {
            "best_z": es.result.xbest,
            "best_fitness": -es.result.fbest,
            "history": history,
        }