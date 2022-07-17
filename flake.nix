{
  description = "A very basic flake";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-22.05";

  outputs = { self, nixpkgs }: 
  let
    pkgs = import nixpkgs { system = "x86_64-linux"; };
  in
  {
    defaultPackage.x86_64-linux = 
      pkgs.python3.pkgs.buildPythonPackage rec {
        pname = "texbld";
        version = "0.3.0";
        src = ./.;
        format = "pyproject";
        propagatedBuildInputs = with pkgs.python3.pkgs;
            [jsonschema docker requests toml urllib3];
        buildInputs = with pkgs; [poetry];
        meta = with pkgs.lib; {
          homepage = "https://texbld.com";
          description = "A Modern Build Tool for Your Papers";
          license = licenses.gpl3;
        };
        doCheck = false;
      };
    devShell.x86_64-linux =
      let
        python_dev_packages = (
          let
            deps = pythonpkgs: with pythonpkgs; 
              [autopep8 pylint poetry];
          in pkgs.python3.withPackages deps
        );
      in
      pkgs.mkShell {
        buildInputs = [python_dev_packages pkgs.scc];
        shellHook = ''
          if ! poetry env info -p 2>&1 > /dev/null; then
            poetry install
          fi
          source `poetry env info -p`/bin/activate
        '';
      };
  };
}
