{
  description = "A Modern Build Tool for Your Papers";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
  };

  outputs = { self, nixpkgs }: 
  let
    pkgs = import nixpkgs { system = "x86_64-linux"; };
    python_dev_packages = (
      let
        deps = pythonpkgs: with pythonpkgs; 
          [jsonschema docker requests toml urllib3 pytest autopep8 pylint poetry];
      in pkgs.python3.withPackages deps
    );
  in
  {
    /*
    defaultPackage.x86_64-linux = 
      pkgs.python3.pkgs.buildPythonPackage rec {
        pname = "texbld";
        version = "0.2.0";
        src = pkgs.python3.pkgs.fetchPypi {
          inherit pname version;
          sha256 = "789e8736146a6be1c2414154db0d0aaa0ff4acc1efd4845d34798e9f6190b92e";
        };
        checkInputs = with pkgs.python3.pkgs;
            [jsonschema docker requests toml urllib3];
        buildInputs = with pkgs.python3.pkgs; [poetry];
        meta = with pkgs.lib; {
          homepage = "https://texbld.com";
          description = "A Modern Build Tool for Your Papers";
          license = licenses.gpl3;
        };
      };
    */
    devShell.x86_64-linux = 
      pkgs.mkShell {
        buildInputs = [python_dev_packages];
      };
  };
}
