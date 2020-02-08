import cx_Freeze

executables = [cx_Freeze.Executable("Game.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["Box.py", "Button.py", "Emotion.py", "Factory.py", "Game.py", "House.py",
                                            "icons8-house-96.png", "icons8-manufacturing-96.png",
                                            "icons8-manufacturing-96vertical.png",
                                            "icons8-sea-waves-96.png", "icons8-tree-96.png", "Sea.py", "setting.py",
                                            "SPRITETYPE.py", "Terrain.txt", "Tree.py"
                                            ]}},
    executables = executables

    )