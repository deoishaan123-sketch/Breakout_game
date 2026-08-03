from turtle import Turtle,Screen
import random
import time


def start_game():
    screen=Screen()
    screen.setup(width=900,height=600)
    screen.title("BREAKOUT")
    screen.bgcolor("#0f172a")
    screen.tracer(0)

    ball = Turtle()
    ball.shape("circle")
    ball.color("#f8fafc")
    ball.penup()
    ball_dx = 10
    ball_dy = -10

    scoreboard = Turtle()
    scoreboard.penup()
    scoreboard.hideturtle()
    scoreboard.color("white")
    scoreboard.goto(0, 260)

    bricks = []

    for row in range(5):
        for col in range(10):
            brick = Turtle()
            brick.shape("square")
            brick_colors = [
                "#ef4444",  # red
                "#f97316",  # orange
                "#eab308",  # yellow
                "#22c55e",  # green
                "#3b82f6"  # blue
            ]
            brick.color(brick_colors[row])
            brick.shapesize(stretch_wid=0.9, stretch_len=2.8)
            brick.penup()

            x = -340 + col * 70
            y = 200 - row * 30

            brick.goto(x, y)
            bricks.append(brick)

    score = 0
    lives = 5

    def update_score():
        scoreboard.clear()
        scoreboard.write(
            f"Score:{score}  Lives:{lives}",
            align="center",
            font=("Arial", 20, "bold")
        )

    paddle = Turtle()
    paddle.shape("square")
    paddle.color("#38bdf8")
    paddle.shapesize(stretch_len=5, stretch_wid=1)
    paddle.speed("fastest")
    paddle.penup()
    paddle.goto(0, -250)

    def paddle_right():
        if paddle.xcor() < 390:
            paddle.setx(paddle.xcor() + 20)

    def paddle_left():
        if paddle.xcor() > -390:
            paddle.setx(paddle.xcor() - 20)

    screen.listen()
    screen.onkeypress(paddle_right, "d")
    screen.onkeypress(paddle_left, "a")

    is_game_on = True
    update_score()

    while is_game_on:
        screen.update()
        time.sleep(0.05)

        ball.goto(ball.xcor() + ball_dx, ball.ycor() + ball_dy)

        if ball.distance(paddle) < 60 and ball.ycor() < -230:
            ball_dy *= -1

        if ball.xcor() > 440 or ball.xcor() < -440:
            ball_dx *= -1

        if ball.ycor() > 290:
            ball_dy *= -1

        if ball.ycor() < -290:
            lives -= 1
            update_score()
            ball.goto(0, 0)
            ball_dx = random.choice([-8, 8])
            ball_dy = random.choice([-6, -4, 4, 6])

        if lives <= 0:
            is_game_on = False
            scoreboard.clear()
            scoreboard.goto(0, 0)
            scoreboard.write("Game Over", align="center", font=("Courier", 30, "bold"))

        for brick in bricks[:]:
            if ball.distance(brick) < 35:
                ball_dy *= -1

                brick.hideturtle()
                bricks.remove(brick)

                score += 10
                update_score()
                break

    screen.update()
    screen.exitonclick()
