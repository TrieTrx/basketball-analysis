# basketball-analysis
- Thought about small objects require large amount of epochs to converge, while large objects like players require fewer epochs -> 2 models, one for player and one for ball.
- I observed that player model (100 epochs) have much better score than ball model (200 epochs) so I use player model for both.

# Ball acquisition
- In case there are more than 1 ball, get 1 with highest confidence score
- There's still some cases where the ball detect somewhere else far away from the ball, we can fix by skipping some frames if the detected ball in one frame is too far away from the one in the previous frame