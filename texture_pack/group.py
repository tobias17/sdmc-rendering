import os, json
import numpy as np
import cv2

nl = "\n"

def lsw(str, pat):
   return str.lower().startswith(pat)

def filter_with_pattern(pat, names):
   return [f for f in names if all(f.startswith(p[1:]) if p.startswith("^") else p.lower() in f.lower() for p in pat.split(" "))]

def main():
   texture_dir = "assets/minecraft/textures/block"

   root_dir = os.environ.get("PACK_DIR")
   if root_dir is None or not os.path.exists(root_dir):
      raise ValueError(f"Could not find root_dir '{root_dir}', make sure the env var is set to a valid version root folder")

   save_dir = f"texture_pack/sdmc-attn-mask/{texture_dir}"
   if not os.path.exists(save_dir):
      os.makedirs(save_dir)

   all_filenames = [f for f in os.listdir(f"{root_dir}/{texture_dir}") if f.endswith(".png")]

   data_filepath = "texture_pack/data.json"
   if os.path.exists(data_filepath):
      with open(data_filepath) as f:
         data = json.load(f)
   else:
      data = { "index": 0, "entries": [] }

   while True:
      text = input("[p]attern, [r]ender, [q]uit: ")
      if lsw(text, "q"):
         return
      elif lsw(text, "p"):
         is_pat = True
         while is_pat:
            pattern = input("Enter your pattern: ")
            pattern_files = filter_with_pattern(pattern, all_filenames)
            print(f"\nPattern would produce:\n{nl.join(pattern_files)}")
            while True:
               text = input("[s]ave, [a]gain, [e]xit: ")
               if lsw(text, "s"):
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
               elif lsw(text, "a"):
                  break
               else:
                  is_pat = False
                  break
      elif lsw(text, "r"):
         rem_filenames = set(all_filenames.copy())
         for entry in data["entries"]:
            entry_filenames = filter_with_pattern(entry["pattern"], rem_filenames)
            for filename in entry_filenames:
               img = cv2.imread(f"{root_dir}/{texture_dir}/{filename}", cv2.IMREAD_UNCHANGED)
               img[:,:,:3] = entry["color"][::-1]
               cv2.imwrite(f"{save_dir}/{filename}", img)
            rem_filenames -= set(entry_filenames)



if __name__ == "__main__":
   main()
