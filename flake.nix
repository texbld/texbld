{
  description = "A Modern Build Tool for Your Papers";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-22.05";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    with flake-utils.lib;
    eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in {
        defaultPackage = pkgs.python3.pkgs.buildPythonPackage rec {
          pname = "texbld";
          version = "0.3.0";
          src = ./.;
          format = "pyproject";
          propagatedBuildInputs = with pkgs.python3.pkgs; [
            jsonschema
            docker
            requests
            toml
            urllib3
          ];
          buildInputs = with pkgs; [ poetry ];
          meta = with pkgs.lib; {
            homepage = "https://texbld.com";
            description = "A Modern Build Tool for Your Papers";
            license = licenses.gpl3;
          };
          doCheck = false;
        };
        devShell = let
          python_dev_packages = (let
            deps = pythonpkgs:
              with pythonpkgs; [
                autopep8
                pylint
                poetry
                jsonschema
                docker
                requests
                toml
                urllib3
                pytest
                pytest-xdist
              ];
          in pkgs.python3.withPackages deps);
        in pkgs.mkShell { buildInputs = [ python_dev_packages pkgs.scc ]; };

        formatter = nixpkgs.legacyPackages."${system}".nixfmt;
      });
}
