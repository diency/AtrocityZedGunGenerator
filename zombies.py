import random

class Zombie:
    def __init__(self, name, number, zp_cost):
        self.name = name
        self.number = number
        self.zp_cost = zp_cost

def fill_zombie_deck():
    return [
        Zombie('Grunt', 5, 2),
        Zombie('Grunt', 6, 2),
        Zombie('Grunt', 7, 2),
        Zombie('Grunt', 8, 2),
        Zombie('Grunt', 10, 2),
        Zombie('Grunt', 11, 2),
        Zombie('Grunt', 12, 2),
        Zombie('Grunt', 13, 2),
        Zombie('Grunt', 14, 2),
        Zombie('Grunt', 15, 2),
        Zombie('Rhino', 5, 4),
        Zombie('Rhino', 6, 4),
        Zombie('Rhino', 7, 4),
        Zombie('Rhino', 8, 4),
        Zombie('Rhino', 12, 4),
        Zombie('Rhino', 15, 4),
        Zombie('Blimp', 1, 4),
        Zombie('Blimp', 12, 4),
        Zombie('Blimp', 15, 4),
        Zombie('Ninja', 1, 5),
        Zombie('Ninja', 4, 5),
        Zombie('Ninja', 9, 5),
        Zombie('Smokescreen', 12, 8),
        Zombie('Smokescreen', 15, 8),
        Zombie('Trebuchet', 1, 8),
        Zombie('Trebuchet', 4, 8),
        Zombie('Trebuchet', 9, 8),
        Zombie('Shrill', 1, 8),
        Zombie('Shrill', 4, 8),
        Zombie('Biohazard', 1, 15),
        Zombie('Biohazard', 4, 15),
        Zombie('Outcast', 4, 15),
        Zombie('Outcast', 9, 15),
        Zombie('Butcher', 1, 15),
        Zombie('Butcher', 2, 15),
        # TODO: add 2 of each boss card, but make it so you can never draw them after drawing for the first time
        """
        Zombie('BOSS - Nerd', 1, 10),
        Zombie('BOSS - Nerd', 1, 10),
        Zombie('BOSS - DJ', 1, 20),
        Zombie('BOSS - DJ', 1, 20),
        Zombie('FINAL BOSS - Atrocity', 1, 40),
        Zombie('FINAL BOSS - Atrocity', 1, 40),
        """

    ]

def refresh(drawp, disp):
    # note that this does NOT completely reset the draw pile
    # if there are cards not currently in the discard pile
    drawp.extend(disp)
    random.shuffle(drawp)
    disp.clear()

def zp_draw(drawp, disp, zp):
    print(f'Drawing {zp} ZP worth of zombies...')
    zp_spent = 0
    upper_bound = zp + 5
    active_zombies = [] # this is to make sure it doesn't duplicate zombies when shuffling mid draw

    # it is theoretically possible for this to get stuck in the while loop, eg zp is 3, and the only card we have in the
    # draw or discard piles costs 10 - it would continually draw and shuffle this card forever
    sanity = 10000
    while zp_spent < zp:
        sanity -= 1
        if sanity <= 0:
            break

        if len(drawp) == 0:
            refresh(drawp, disp)
            # drew literally every card!
            if len(drawp) == 0:
                break
        zed = drawp[0]
        zed_cost = zed.zp_cost
        if zp_spent + zed_cost > upper_bound:
            # too expensive!
            disp.append(zed)
            drawp.pop(0)
        else:
            zp_spent += zed_cost
            active_zombies.append(zed)
            drawp.pop(0)

    # sort active cards by name then number, then print
    active_zombies.sort(key=lambda z: (z.name, z.number))
    for zombie in active_zombies:
        print(f'{zombie.name} - {zombie.number}')

    disp.extend(active_zombies)

    return drawp, disp

if __name__ == '__main__':

    zp = 3
    zp_inc = 6

    draw_pile = fill_zombie_deck()
    random.shuffle(draw_pile)
    discard_pile = []

    # "drawing" a card moves it from draw to discard, and prints it

    while True:
        user_input = input("Enter command - type 'help' for list of commands: ")  # Read user input
        args = user_input.split()  # Split input into arguments

        if not args:
            continue  # Skip empty input

        command = args[0].lower()  # First argument as command

        print("=====================")
        match command:
            case "help":
                print("help - prints this")
                print("exit - terminates the program (THIS WILL DELETE YOUR STUFF!!)")
                print("")
                print("zp (a) - sets zp to (a) for shop/item gen, default value is 3")
                print("zpinc (a) - sets zp increment per next round to (a), default value is 6")
                print("")
                print("horde - continually draws cards based on zp, then increase zp by zpinc")
                print("summon - continually draws cards based on zp, does NOT increase zp")
                print("draw (a) - draws (a) cards (or just one if no args provided)")
                print("shuffle - shuffles the discard pile back into the draw pile")
            case "exit":
                print("Goodbye!")
                break
            case "zp":
                zp = int(args[1])
                print(f"zp set to {args[1]}")
            case "zpinc":
                zp_inc = int(args[1])
                print(f'zp increment set to {args[1]}')
            case "horde":
                draw_pile, discard_pile = zp_draw(draw_pile, discard_pile, zp)
                zp += zp_inc
            case "summon":
                draw_pile, discard_pile = zp_draw(draw_pile, discard_pile, zp)
            case "draw":
                if len(args) == 1:
                    draw_amount = 1
                else:
                    draw_amount = args[1]

                for i in range(draw_amount):
                    # shuffle if no cards to draw
                    if len(draw_pile) == 0:
                        refresh(draw_pile, discard_pile)
                    zomb = draw_pile[0]
                    print(f'{zomb.name} - {zomb.number}')
                    discard_pile.append(zomb)
                    draw_pile.pop(0)
            case "shuffle":
                print('shuffling discard pile back into draw pile...')
                refresh(draw_pile, discard_pile)
        print("=====================")