# Folder-Synchronisation
Using Google API

#Clone Wars 2.0
Prime Minister Lama Su,

I hope this letter finds you in the best of health.

The last batch of clones you built for us were faulty and did not perform as expected (https://www.youtube.com/watch?v=b0DuUnhGBK4)

We unearthed some secrets about how the droid army was trained and hope that you can use this information to make a better army this time around. With the galaxy on the brink of another war, I cannot help but emphasize how much a large discount will help the Republic in its efforts.

One of our allies came across these schematics in an abandoned base that shed some light on the droid training exercises, master Yoda concluded that a pair of droids undergo various kinds of battle simulations during which each droid records its progress and learning in a force, currently unfamilair to us, called "Data". This force from both droids is then combined in a ritual called the "Sync" resulting in both droids having an increased data force.

Please have a look at this schematic, your engineers may have better luck decoding its mysteries.

        +----------------+                +----------------+
        |                |                |                |
        |   +--------+   |      Sync      |   +--------+   |
        |   |-|Data|-|   | +------------> |   |-|Data|-|   |
        |   +--------+   | <------------+ |   +--------+   |
        |                |                |                |
        |    Driod  A    |                |    Driod  B    |
        |                |                |                |
        +----------------+                +----------------+
May the force be with you.

Sifo-Dyas
[....2 months later....]

Prime Minister Lama Su!,

I hope the army is coming along nicely. The force has given us more clarity in the last few months. As it turns out, this "Data" that we were so worried about, is just a method by which the droids store information about their experiences and orders. Most importantly, the "Sync" ritual was just an exchange of files from one droid to another in both directions. This is how their data force increased after the ritual.

Master Windoo has been doing extensive research and has come up with a simplified experiment to test if this training method can be implemented. He says that you should start by figuring out how to synchronize data between a folder on one device (say device A) and a folder on another device (say device B). In addition to that, a change made to the data on one device should also be made available to the other device as well. If we have a way to do this then we could potentially improve the quality of the new clone army. I hope your engineers are able to make sense of all of this information. Do write back to me if you need more information.

Please share your method and implementation in great detail with us so that it can be added to our records in the Jedi Temple. I wish you luck.

May the force be with you.

Sifo-Dyas
                                 +---------------------+
                                 | Whats going on here?|
                                 +------------------+--+
                                                    |
                                                    |
  _                                                 |
  \\                                                |
   \\_          _.-._                               |
    X:\        (_/ \_)     <------------------------+
    \::\       ( ==  )
     \::\       \== /
    /X:::\   .-./`-'\.--.
    \\/\::\ / /     (    l
     ~\ \::\ /      `.   L.
       \/:::|         `.'  `
       /:/\:|          (    `.
       \/`-'`.          >    )
              \       //  .-'
               |     /(  .'
               `-..-'_ \  \
               __||/_ \ `-'
              / _ \ #  |
             |  #  |#  |   B-SD3 Security Droid
          LS |  #  |#  |      - Front View -
          
Steps:
1. Install dependencies
$ pip install --upgrade google-api-python-client

$ pip install watchdog

2. Run python file in the folder which you want to synchronize your drones to.

3. Run python file in the drone folder.
