{ pkgs ? import <nixpkgs> {} }:
pkgs.python3.pkgs.buildPythonPackage rec {
  pname = "texbld";
  version = "0.2.1";
  src = pkgs.python3.pkgs.fetchPypi {
    inherit pname version;
    sha256 = "2eec96b55143d61131e21362b8e8016f800b4f36a34e3364a220d0634a66b5db";
  };

  propagatedBuildInputs = with pkgs.python3.pkgs;
      [jsonschema docker requests toml urllib3];
  meta = with pkgs.lib; {
    homepage = "https://texbld.com";
    description = "A Modern Build Tool for Your Papers";
    license = licenses.gpl3;
  };
  doCheck = false;
}
