{ pkgs ? import <nixpkgs> {} }:
let
  python_dev_packages = (
    let
      deps = pythonpkgs: with pythonpkgs; 
        [autopep8 pylint poetry];
    in pkgs.python3.withPackages deps
  );
in
pkgs.mkShell {
  buildInputs = [python_dev_packages];
  shellHook = ''
    if ! poetry env info -p; then
      poetry install
    fi
    source `poetry env info -p`/bin/activate
  '';
}