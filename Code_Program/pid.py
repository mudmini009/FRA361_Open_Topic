# simple P-ID controller
class PID:
    def __init__(self, kp, ki=0.0, kd=0.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        self.prev_err = 0.0

    def update(self, error, dt):
        self.integral += error * dt
        deriv = (error - self.prev_err) / dt if dt > 0 else 0.0
        self.prev_err = error
        return (
            self.kp * error +
            self.ki * self.integral +
            self.kd * deriv
        )