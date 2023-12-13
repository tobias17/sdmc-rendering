import os, json
import numpy as np
import cv2

nl = "\n"

def lsw(str, pat):
   return str.lower().startswith(pat)

def main():
   texture_dir = "assets/minecraft/textures/block"

   root_dir = os.environ.get("PACK_DIR")
   if root_dir is None or not os.path.exists(root_dir):
      raise ValueError(f"Could not find root_dir '{root_dir}', make sure the env var is set to a valid version root folder")

   save_dir = f"texture_pack/sdmc-attn-mask/{texture_dir}"
   if not os.path.exists(save_dir):
      os.makedirs(save_dir)

   all_filenames = os.listdir(f"{root_dir}/{texture_dir}")

   data_filepath = "data.json"
   if os.path.exists(data_filepath):
      with open(data_filepath) as f:
         data = json.load(f)
   else:
      data = { "index": 0, "entries": [] }

   while True:
      text = input("[p]attern, [q]uit: ")
      if text.lsw("q"):
         return
      elif text.lsw("p"):
         is_pat = True
         while is_pat:
            pattern = input("Enter your pattern: ")
            pattern_files = [f for f in all_filenames if pattern in all_filenames]
            print(f"Pattern would produce:\n{nl.join(pattern_files)}")
            while True:
               text = input("[s]ave, [a]gain, [e]xit: ")
               if text.lsw("s"):
                  prompt = input("Enter a prompt: ")
                  data["entries"].append({
                     "pattern": pattern,
                     "prompt": prompt,
                     "color": [0, data["index"]//256, data["index"]%256]
                  })
                  data["index"] += 1
                  with open(data_filepath, "w") as f:
                     json.dump(data, f, indent="\t")
                  is_pat = False
                  break
               elif text.lsw("a"):
                  break
               else:
                  is_pat = False
                  break


if __name__ == "__main__":
   main()
