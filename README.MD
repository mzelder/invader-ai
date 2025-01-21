# Q-Learning Model
[FirstGen](gens/first_gen.pth)
<br><br>
Current model played 200 games with 3 bullets appearing on the screen. [here](images/image1.png)
<br><br>
Current model played 1k games with 5 bullets appearing on the screen. [here](images/image2.png). [chart](images/chart2.png)
At the start model played better than after few hundreds games. I will try to change rewarding system.
So the longer it will live the more points he will get.
<br><br>
I tried to train new [model](gens/gen2.pth) after 4,5k games (3h). He doesnt learn a thing [chart](images/chart3.png)
<br><br>

# Gen 4 and 4 are relateted which each other
[Gen3](gens/gen3.pth)
After 1k games this is [chart](images/chart4.png). Model surely evolved. I think this is good direction to learn him.<br>
Bullet speed was set up on 10px per move.
5 bullets plus 2 additional on left and right eq 7

Rwarding system:
- +3 in safe zone
- -1 in danger zone

[Gen4](gens/gen4.pth)
Night training 3,5k tries. [chart](images/chart5.png)
Bullet speed was set up on 20px per move.
5 bullets plus 2 additional on left and right eq 7
Iam not sure if he learn something becuase of stagnation he get and the average also wasnt going up.

