{ pkgs ? import <nixpkgs> {} }:
pkgs.python3.pkgs.buildPythonPackage rec {
  pname = "texbld";
  version = "0.3.dev0";
  src = ./dist/texbld-0.3.dev0.tar.gz;

  propagatedBuildInputs = with pkgs.python3.pkgs;
      [jsonschema docker requests toml urllib3];
  meta = with pkgs.lib; {
    homepage = "https://texbld.com";
    description = "A Modern Build Tool for Your Papers";
    license = licenses.gpl3;
  };
  doCheck = false;
}
