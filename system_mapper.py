import os
import inspect
import importlib
import pkgutil
from pathlib import Path

class SystemMapper:
    def __init__(self):
        self.root_path = Path(__file__).parent.absolute()
        self.target_folders = ["core", "interfaces", "engines"]

    def _get_module_content(self, module_name):
        inventory = {"classes": {}, "functions": []}
        try:
            mod = importlib.import_module(module_name)
            # 1. Quét Class
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if obj.__module__ == module_name:
                    methods = [m[0] for m in inspect.getmembers(obj, inspect.isroutine) 
                               if not m[0].startswith('_')]
                    inventory["classes"][name] = methods
            # 2. Quét hàm standalone
            for name, obj in inspect.getmembers(mod, inspect.isfunction):
                if obj.__module__ == module_name:
                    inventory["functions"].append(name)
            return inventory
        except Exception:
            return None

    def scan(self):
        print("\n" + "═"*85)
        print(f"🏗️  PROJECT STRUCTURE TREE: {self.root_path.name.upper()}")
        print("═"*85)

        for folder in self.target_folders:
            folder_path = self.root_path / folder
            if not folder_path.exists(): continue

            print(f"\n📂 {folder}/")
            
            modules = list(pkgutil.iter_modules([str(folder_path)]))
            for i, (loader, mod_name, is_pkg) in enumerate(modules):
                is_last_mod = (i == len(modules) - 1)
                prefix_mod = "└── " if is_last_mod else "├── "
                pipe_mod = "    " if is_last_mod else "│   "
                
                print(f"{prefix_mod}📄 {mod_name}.py")
                
                content = self._get_module_content(f"{folder}.{mod_name}")
                
                # Kiểm tra xem file có hoàn toàn trống không
                if not content or (not content["functions"] and not content["classes"]):
                    print(f"{pipe_mod}    └── ⚠️  Empty File (No logic yet)")
                    continue

                # In Standalone Functions
                for j, func in enumerate(content["functions"]):
                    is_last_func = (j == len(content["functions"]) - 1 and not content["classes"])
                    prefix_f = "    └── ƒ " if is_last_func else "    ├── ƒ "
                    print(f"{pipe_mod}{prefix_f}{func}()")

                # In Classes & Methods
                class_list = list(content["classes"].items())
                for k, (cls_name, methods) in enumerate(class_list):
                    is_last_cls = (k == len(class_list) - 1)
                    prefix_c = "    └── 🏛️ " if is_last_cls else "    ├── 🏛️ "
                    pipe_c = "        " if is_last_cls else "    │   "
                    
                    if not methods:
                        print(f"{pipe_mod}{prefix_c}{cls_name} (⚠️  Empty Class)")
                    else:
                        print(f"{pipe_mod}{prefix_c}{cls_name}")
                        for l, method in enumerate(methods):
                            is_last_m = (l == len(methods) - 1)
                            prefix_m = "└── " if is_last_m else "├── "
                            print(f"{pipe_mod}{pipe_c}{prefix_m}{method}()")

        # 2. Quét thư mục gốc
        print("\n🎮 ROOT_CONTROLLERS/")
        root_files = [f for f in self.root_path.glob("*.py") 
                      if f.name not in ["system_mapper.py", "app.py", "config.py"]]
        
        for i, file in enumerate(root_files):
            is_last_root = (i == len(root_files) - 1)
            prefix_rf = "└── " if is_last_root else "├── "
            print(f"{prefix_rf}📄 {file.name}")
            
            content = self._get_module_content(file.stem)
            if not content or (not content["functions"] and not content["classes"]):
                print(f"    └── ⚠️  Empty File")
                continue

            for cls_name, methods in content["classes"].items():
                if not methods:
                    print(f"    └── 🏛️ {cls_name} (⚠️  Empty Class)")
                else:
                    print(f"    └── 🏛️ {cls_name}")
                    for m in methods:
                        print(f"        ├── {m}()")
            
            for f_name in content["functions"]:
                print(f"    └── ƒ {f_name}()")

        print("\n" + "═"*85)
        print("✅ DONE! Hãy soi kỹ các mục ⚠️  để hoàn thiện code nhé Vũ.")

if __name__ == "__main__":
    mapper = SystemMapper()
    mapper.scan()

    # giới thiệu Python, cài đặt Python, và thực hiện code "Hello World" trong môi trường Visual Studio Code (VSC)