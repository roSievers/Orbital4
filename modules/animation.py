"""This module provides provides animations for static and moving objects"""

from pygame import Rect

class Animator(object):
    __slots__ = ["startTime"]
    def __init__(self, time):
        object.__init__(self)
        self.startTime = time
    def evaluate(self, time):
        """The time parameter should always be bigger than the last time,
        because some animators delete useless detail""" 
        raise NotImplementedError("The base Animator provides no animation.")
    def getDelta(self, time):
        return time - self.startTime
    
class StaticAnimator(Animator):
    __slots__ = ["rect"]
    def __init__(self, time, rect):
        Animator.__init__(self, time)
        self.rect = rect
    def evaluate(self, time):
        return self.rect
    
class FlowAnimator(Animator):
    """Animator shifting between two Animators,
    supports StaticAnimator and FlowAnimator"""
    __slots__ = ["start", "end", "length"]
    def __init__(self, time, length, start, end):
        Animator.__init__(self, time)
        self.length = length
        self.start, self.end = start, end
    def evaluate(self, time):
        start = self.start.evaluate(time)
        
        # check, whether the animator has finished
        if isinstance(self.start, FlowAnimator):
            if self.start.getDelta(time) > self.start.length:
                self.start = StaticAnimator(time, start)
        
        end = self.end.evaluate(time)
        
        # check, whether the animator has finished
        if isinstance(self.end, FlowAnimator):
            if self.end.getDelta(time) > self.end.length:
                self.end = StaticAnimator(time, end)
                
        t = min(max( self.getDelta(time) * 1.0 / self.length, 0), 1)
        
        left   = round( start.left   * (1-t) + end.left   * t )
        top    = round( start.top    * (1-t) + end.top    * t )
        width  = round( start.width  * (1-t) + end.width  * t )
        height = round( start.height * (1-t) + end.height * t )
        
        return Rect((left, top), (width, height))