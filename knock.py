class Knock(object):
    def __init__(self, question, expected=None):
        self.Q = question.replace("Permalink\n","：")
        self.expected = expected
        self.A = None

    def display(self):
        display(self.Q)
        arr = [f"回答：", self.A]
        
        if callable(self.expected) and self.A:
            arr.append(f"採点：")
            arr.append(self.expected(self.A))
        elif self.expected and self.A:
            arr = [f"正答：", self.expected, *arr]
            arr.append(f"採点：")
            arr.append(self.expected == self.A)
        else:
            arr.append(f"（正答なし）")
        [display(t) for t in arr]
