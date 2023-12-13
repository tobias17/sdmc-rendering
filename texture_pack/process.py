from sentence_transformers import SentenceTransformer # type: ignore
import os, csv
import numpy as np
import cv2


def get_embedding(text):
   if not hasattr(get_embedding, 'model'):
      get_embedding.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
   return get_embedding.model.encode([text])[0]

def load_all_data():
   all_data = []
   with open("texture_pack/color_codes.csv") as f:
      reader = csv.reader(f)
      for color_str, label_str in reader:
         color = [int(c.strip()) for c in color_str.strip("()").split(",")][::-1]
         label = " ".join(label_str.split(";"))
         embed = get_embedding(label)
         all_data.append({
            "label": label,
            "color": color,
            "embed": embed,
         })
   return all_data

def main():
   texture_dir = "assets/minecraft/textures/block"
   all_data = load_all_data()

   root_dir = os.environ.get("PACK_DIR")
   if root_dir is None or not os.path.exists(root_dir):
      raise ValueError(f"Could not find root_dir '{root_dir}', make sure the env var is set to a valid version root folder")

   save_dir = f"texture_pack/sdmc-color-codes/{texture_dir}"
   if not os.path.exists(save_dir):
      os.makedirs(save_dir)

   all_filenames = os.listdir(f"{root_dir}/{texture_dir}")
   all_filenames = [f for f in all_filenames if any(f.startswith(c) for c in ['s', 't'])]

   for filename in sorted(all_filenames):
      if not filename.endswith(".png"):
         continue

      in_path  = f"{root_dir}/{texture_dir}/{filename}"
      out_path = f"{save_dir}/{filename}"
      if os.path.exists(out_path):
         continue

      label = filename.replace(".png", "").replace("_", " ")
      print(label)

      def make_sorted_deltas(text):
         embed = get_embedding(text)
         deltas = [(i,np.mean(np.abs(d["embed"] - embed))) for i,d in enumerate(all_data)]
         return sorted(deltas, key=lambda x: x[1])
      sorted_deltas = make_sorted_deltas(label)
      for i in range(9):
         print(f"{i+1}: {all_data[sorted_deltas[i][0]]['label']}")

      img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
      cv2.imshow("img", img)
      while True:
         key = cv2.waitKey()
         if key == 113: # q
            cv2.destroyAllWindows()
            return
         elif key >= 49 and key <= 57: # 1-9
            index = key-49
            color = all_data[sorted_deltas[index][0]]['color']
            img[:,:,:3] = color
            cv2.imwrite(out_path, img)
            break
         elif key == 115: # s
            break
         elif key == 110: # n
            print(label)
            sorted_deltas = sorted_deltas[9:]
            for i in range(9):
               print(f"{i+1}: {all_data[sorted_deltas[i][0]]['label']}")
         elif key == 116: # t
            text = input("new label: ")
            sorted_deltas = make_sorted_deltas(text)
            for i in range(9):
               print(f"{i+1}: {all_data[sorted_deltas[i][0]]['label']}")
         else:
            print(key)


if __name__ == "__main__":
   main()
