{
  description = "A Modern Build Tool for Your Papers";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-22.05";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    with flake-utils.lib;
    eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        version = "0.4.dev0";
      in {
        defaultPackage = pkgs.python3.pkgs.buildPythonPackage rec {
          inherit version;
          pname = "texbld";
          src = ./.;
          format = "pyproject";
          propagatedBuildInputs = with pkgs.python3.pkgs; [
            jsonschema
            docker
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
        packages = flattenTree {
          zipapp = let
            custompython = pkgs.python39.withPackages
                (ps: with ps; [ jsonschema docker toml urllib3 shiv poetry ]);
            in
            pkgs.stdenv.mkDerivation {
              inherit version;
              src = ./.;
              name = "texbld-zipapp";
              buildInputs = [ custompython pkgs.poetry ];
              phases = [ "configurePhase" "buildPhase"];
              configurePhase = ''
                cd $src
                mkdir -p $out
                cp -Lr ${custompython}/${custompython.sitePackages} $out/dist
                chmod -R +w $out/dist
                cp -Lr $src/* $out/dist/
                chmod -R +w $out/dist
              '';
              buildPhase = ''
                cd $src
                ${pkgs.python39.pkgs.shiv}/bin/shiv --compressed --site-packages $out/dist -o $out/texbld.pyz -e texbld.cli.run
                sha256sum -b $out/texbld.pyz > $out/texbld.pyz.sha256sum
                rm -rf $out/dist
              '';
              doCheck = false;
            };
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
                shiv
              ];
          in pkgs.python3.withPackages deps);
        in pkgs.mkShell { buildInputs = [ python_dev_packages pkgs.scc ]; };

        formatter = nixpkgs.legacyPackages."${system}".nixfmt;
      });
}
