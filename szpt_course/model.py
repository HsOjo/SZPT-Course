class CourseModel:
    def __init__(self, **kwargs):
        self._fields = []
        self.type: str = ''
        self.class_: str = ''
        self.course: str = ''
        self.teacher: str = ''
        self.teacher_spare: str = ''
        self.place: str = ''
        self.remark: str = ''
        self.week: int = -1
        self.day: int = -1
        self.node_num: int = -1
        for k, v in kwargs.items():
            self._fields.append(k)
            setattr(self, k, v)

    @property
    def data(self):
        r = {}
        for k in self._fields:
            r[k] = getattr(self, k)
        return r

    def __repr__(self):
        return super().__repr__() + '\n\t%s' % self.data
