from . import option
from .base import Docker_Base

class Docker_Build(Docker_Base):
    def __init__(self, opt):
        super(Docker_Build, self).__init__(opt)
        self.set_cmd()

    def set_cmd(self):
        self.format = f'docker build -t {self.opt.image} --build-arg passwd="$(cat /etc/passwd)" -f {self.opt.dockerfile} .'

def main():
    opt = option.Options().get_option()
    docker = Docker_Build(opt)
    docker.print_cmd()
    docker.do_cmd()

if __name__ == '__main__':
    main()
