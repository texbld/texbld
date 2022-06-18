from dataclasses import dataclass, field
from texbld.common.exceptions import DependencyCycle
from texbld.common.image import Image


@dataclass
class Solver:
    image: 'Image'
    build_seq: 'list[Image]' = field(init=False)

    def __post_init__(self):
        encountered_hashes: 'set[str]' = set()
        self.build_seq = [self.image]
        while True:
            current_hash = self.build_seq[-1].image_hash()
            if current_hash in encountered_hashes:
                raise DependencyCycle(self.build_seq)
            else:
                encountered_hashes.add(current_hash)
            if self.build_seq[-1].is_base():
                break
            self.build_seq[-1].pull()
            # everything after this step can only be done if our image actually has a dependency.
            self.build_seq.append(self.build_seq[-1].get_source().inherit)

    def images(self):
        return self.build_seq
