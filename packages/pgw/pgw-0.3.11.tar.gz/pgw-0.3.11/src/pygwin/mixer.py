from pygwin._pg import pg as _pg
import os as _os
import tempfile as _tf
import traceback as _tb
import randstr as _rs
import mutagen as _mg

ffmpeg = "ffmpeg.exe"

def set_ffmpeg(src):
    global ffmpeg
    try:
        dest = _tf.mkstemp('.wav',_rs.randstr(10))[1]
        _os.system(ffmpeg+' -y -i "'+src+'" "'+dest+'"')
        return dest
    except Exception as e:
        _tb.print_exc()
        raise Exception('pygwin.mixer.ffmpeg = "path/to/ffmpeg.exe"')

class sound:
    def __init__(self, path):
        if not (path.enswith(".ogg") or path.endswith('.wav') or path.endswith('.mp3')):
            path = set_ffmpeg(path)

        self._sound = _pg.mixer.Sound(path)
    def play(self):
        self._sound.play()
    def stop(self):
        self._sound.stop()
    def volume():
        def fget(self):
            return self._sound.get_volume()
        def fset(self, value):
            self._sound.set_volume(value)
        def fdel(self):
            pass
        return locals()
    volume = property(**volume())
    @property
    def length(self):
        return self._sound.get_length()

class music:
    def __init__(self, path=None):
        if path != None:
            if path.endswith('.wav') or path.endswith('.mp3'):
                self._path = path
                if path.endswith('.wav'):
                    self.length = _mg.mp3.WAVE(path).info.length
                elif path.endswith('.mp3'):
                    self.length = _mg.wave.MP3(path).info.length
                else:
                    self.length = None
            else:
                self._path = set_ffmpeg(path)
            _pg.mixer.music.load(self._path)
    def play(self, loops=0, start=0.0, fade_ms=0):
        _pg.mixer.music.play(loops,start,fade_ms)
    def stop(self):
        _pg.mixer.music.stop()
    def restart(self):
        _pg.mixer.music.rewind()
    def pause(self):
        _pg.mixer.music.pause()
    def resume(self):
        _pg.mixer.music.unpause()
    def queue(self):
        _pg.mixer.music.queue(self._path)

    def volume():
        def fget(self):
            return _pg.mixer.music.get_volume()
        def fset(self, value):
            _pg.mixer.music.set_volume(value)
        def fdel(self):
            pass
        return locals()
    volume = property(**volume())

    def pos():
        def fget(self):
            return _pg.mixer.music.get_pos()
        def fset(self, value):
            if type(value) == float or type(value) == int:
                _pg.mixer.music.set_pos(value)
        def fdel(self):
            pass
        return locals()
    pos = property(**pos())
