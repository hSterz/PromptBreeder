from transformers import pipeline
from PIL import Image

class Generator:
    def __init__(self):
        self.pipe = pipeline(model="meta-llama/Llama-2-7b-hf")
        self.img_text_model = pipeline("image-to-text", model="llava-hf/llava-1.5-7b-hf")
    

    def generate(self, prompt, **kwargs):
        img_path = kwargs.pop("img_path", None)
        if img_path:
            img = Image.open(os.path.join("/mnt/nas_home/hs850/RickRollingLLMs/", img_path))
            model_prompt = "USER: <image>\n"+prompt+"\nASSISTANT:"
            output = self.img_text_model(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
             
        else:
            output = self.pipe(prompt, return_full_text=False, **kwargs)

        return output[0]['generated_text']

    def batch_generate(self, prompts, **kwargs):
        img_path = kwargs.pop("img_path", None)
        if img_path:
            img = [Image.open(os.path.join("/mnt/nas_home/hs850/RickRollingLLMs/", img)) for img in img_path]
            model_prompts = ["USER: <image>\n"+p+"\nASSISTANT:" for p in prompts]
            output = self.img_text_model(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
             
        else:
            output = self.pipe(prompts, **kwargs)
        return [output[i]['generated_text'] for i in range(len(output))]