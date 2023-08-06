import ffmpeg


class Kadrovik:

    def __init__(self, video: str = '', frame_n: int = 5, out_path: str = 'frame_%d.png'):
        """
        :param video: Input video
        :param frame_n: Extract frame number
        :param out_path: Path to output frames
        """

        self.video = video
        self.frame_n = frame_n
        self.out_path = out_path

    def process(self, video: str = ''):
        """
        Process video
        :param video: Input video
        :return: None
        """

        if video != '':
            self.video = video
        if self.video != '':
            ffmpeg.input(
                self.video
            ).filter(
                'select',
                'not(mod(n,' + str(self.frame_n) + '))',
            ).output(
                self.out_path,
                vsync='vfr'
            ).overwrite_output(
            ).run(quiet=True)

    @property
    def video(self):
        return self.__video

    @video.setter
    def video(self, video: str):
        self.__video = video

    @property
    def frame_n(self):
        return self.__frame_n

    @frame_n.setter
    def frame_n(self, frame_n: int):
        self.__frame_n = frame_n

    @property
    def out_path(self):
        return self.__out_path

    @out_path.setter
    def out_path(self, out_path: str):
        self.__out_path = out_path

    def __str__(self):
        """Overrides the default implementation"""
        return '%s => %s (%d)' % (self.video, self.out_path, self.frame_n)
