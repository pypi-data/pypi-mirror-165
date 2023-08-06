import ffmpeg


class StreamSaver:

    def __init__(self,
                 stream_URL: str = '',
                 output_template: str = 'output_%Y-%m-%d_%H-%M-%S.ts',
                 segment_time: str = '01:00:00'):
        """
        :param stream_URL: Stream URL
        :param output_template: Output template
        :param segment_time: Segment length
        """

        self.stream_URL = stream_URL
        self.output_template = output_template
        self.segment_time = segment_time
        self.__stream = None

    def run(self, stream_URL: str = '') -> None:
        """
        Start stream saving
        :param stream_URL:
        :return: None
        """

        if stream_URL != '':
            self.stream_URL = stream_URL
        if self.stream_URL != '':
            self.__stream = ffmpeg.input(
                self.stream_URL
            ).output(
                self.output_template,
                vcodec='copy',
                acodec='copy',
                reset_timestamps=1,
                strftime=1,
                f='segment',
                segment_time=self.segment_time,
                segment_atclocktime=1
            ).overwrite_output(
            ).run_async()

    def stop(self) -> None:
        """
        Stop stream
        :return: None
        """
        self.__stream.terminate()

    @property
    def stream_URL(self):
        return self.__stream_URL

    @stream_URL.setter
    def stream_URL(self, stream_URL: str):
        self.__stream_URL = stream_URL

    @property
    def output_template(self):
        return self.__output_template

    @output_template.setter
    def output_template(self, output_template: str):
        self.__output_template = output_template

    @property
    def segment_time(self):
        return self.__segment_time

    @segment_time.setter
    def segment_time(self, segment_time: str):
        self.__segment_time = segment_time

    def __str__(self):
        """Overrides the default implementation"""
        return '%s => %s (%s)' % (self.stream_URL, self.output_template, self.segment_time)
