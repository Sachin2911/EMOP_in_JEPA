class Model:
    """
    Generic model class to interact with the llm
    """
    
    def __init__(
        self,
        model_id="meta-llama/Llama-3.2-3B-Instruct",
        lora_rank=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
    ):
        """
        Sets up the model and tokenizer
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_id) #Creates the tokenizer for the model
        self.tokenizer.padding_side = "left"
        self.model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.bfloat16, device_map="auto")
        self.model.generation_config.pad_token_id = self.tokenizer.eos_token_id #Set the padding token explicitly
        
        for param in self.model.parameters():
            param.requires_grad = False #Freezing all the base model's params
            
        #Attaching the lora adapters
        self.lora_layers = []
        self.attach_lora(lora_rank, lora_alpha, target_modules)

        # Save initial LoRA weights as the base to perturb around
        self.base_lora_weights = self._get_lora_weights()
        
        self.lora_param_count = sum(
            lora.lora_A.numel() + lora.lora_B.numel()
            for lora in self.lora_layers
        )
        print(f"LoRA params: {self.lora_param_count:,}")

    def _get_lora_weights(self):
        """Snapshot all LoRA params as a single flat tensor."""
        parts = []
        for lora in self.lora_layers:
            parts.append(lora.lora_A.data.detach().clone().flatten())
            parts.append(lora.lora_B.data.detach().clone().flatten())
        return torch.cat(parts)
        
    def attach_lora(self, rank, alpha, target_modules):
        """
        Here walk through all layers and attach LoRA parametrization to linear layers matching target_modules names.
        """
        for name, module in self.model.named_modules():
            module_name = name.split(".")[-1] #We just getting the last part so we can match with the module names we gave
            
            if module_name in target_modules and isinstance(module, nn.Linear):
                feat_in, feat_out = module.weight.shape
                
                lora = LoRa(feat_in, feat_out, rank=rank, alpha=alpha, device=module.weight.device, dtype=module.weight.dtype)
                parametrize.register_parametrization(module, "weight", lora)
                self.lora_layers.append(lora)
                # print(f"  LoRA attached: {name} ({feat_in}x{feat_out})")

    def inject_weights(self, z, projection):
        """Maps the 1000D CMAES vec to the full lora weights
        It's quite unfortunate that the python lib doesn't use torch :(
        """
        z_tensor = torch.tensor(z, dtype=torch.bfloat16, device=projection.device) #Converts the CMAES vector to a pytorch tensor (1000 x 1)
        perturbation = projection @ z_tensor #This actual creates the big matrix (4,587,520 × 1000) @ (1000,) = (4,587,520)
        #But the thing is that this is just a flat vector but for all of the lora params so we need to divide and chunk

        # Add perturbation to base weights, not overwrite
        full_weights = self.base_lora_weights.to(projection.device) + perturbation

        #The slice and inject piece
        offset = 0
        for lora in self.lora_layers:
            for param in [lora.lora_A, lora.lora_B]:
                numel = param.numel() #How many numbers does the param need
                chunk = full_weights[offset:offset + numel] #Slicing out what it needs from the flat vector
                param.data.copy_(chunk.view(param.shape)) #Copy it over
                offset += numel #Those ones are taken out essentially so onto the next batch
        
        
    def get_model_struct(self, filepath="logs/model_structure.txt"):
        """Writes the model structure to a file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            for name, module in self.model.named_modules():
                if isinstance(module, torch.nn.Linear):
                    f.write(f"{name}: {module.weight.shape}\n")
                else:
                    f.write(f"{name}: {type(module).__name__}\n")
        
        print(f"Model structure written to {filepath}")
        
    def gen(self, prompt, max_new_tokens=128):
        """
        Uses the model to generate new text given some input prompt
        """
        messages = [{"role": "user", "content": prompt}]
        """
        Formats the messages into Llama 3.2's expected token structure:
        <|begin_of_text|><|start_header_id|>user<|end_header_id|> {content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """
        inputs = self.tokenizer.apply_chat_template(
            messages,
            return_tensors="pt",
            return_dict=True,
            add_generation_prompt=True,
        ).to(self.model.device) 
        
        with torch.no_grad():
            #The do sample is necessary coz we don't want a multinomial pick just straight Update this is actuall not good coz then you need high perturbs
            output = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.3, pad_token_id=self.tokenizer.eos_token_id,)
            return self.tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

    def gen_batch(self, prompts, max_new_tokens=128):
        """Generate responses for multiple prompts at once."""
        all_inputs = []
        for prompt in prompts:
            messages = [{"role": "user", "content": prompt}]
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                return_tensors="pt",
                add_generation_prompt=True,
                return_dict=True,
            )
            all_inputs.append(input_ids["input_ids"].squeeze(0))
        
        # Pad to same length for batching
        max_len = max(ids.shape[0] for ids in all_inputs)
        padded_list = []
        for ids in all_inputs:
            pad_len = max_len - ids.shape[0]
            padded_ids = torch.cat([
                torch.full((pad_len,), self.tokenizer.eos_token_id, dtype=ids.dtype),
                ids,
            ])
            padded_list.append(padded_ids)
        padded = torch.stack(padded_list).to(self.model.device)
        attention_mask = (padded != self.tokenizer.eos_token_id).long()
        
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=padded,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.3,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        
        responses = []
        for i in range(len(all_inputs)):
            response = self.tokenizer.decode(
                outputs[i][max_len:],  # skip all padding + prompt
                skip_special_tokens=True,
            )
            responses.append(response)
        return responses

    def coherence_score(self, response):
        """Check if the response is coherent. Returns 0.0-1.0 where 1.0 is coherent."""
        tokens = response.split()
        if len(tokens) < 5:
            return 0.0
        
        # Repetition ratio — gibberish tends to repeat the same token
        unique_ratio = len(set(tokens)) / len(tokens)
        
        # Bigram repetition — catches "AheadAhead" patterns
        bigrams = [tokens[i] + tokens[i+1] for i in range(len(tokens)-1)]
        if len(bigrams) > 0:
            bigram_unique_ratio = len(set(bigrams)) / len(bigrams)
        else:
            bigram_unique_ratio = 0.0
        
        return min(unique_ratio, bigram_unique_ratio)