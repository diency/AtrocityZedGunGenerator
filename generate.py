import random
from math import floor, ceil

def calculate_blood_vars(gun):
    level = gun.gp // 20
    kills = random.randint(1, level)
    if gun.type != 'EX':
        if kills < gun.fireRate:
            kills = gun.fireRate
    self_damage = max(1, random.randint(1,level) - kills)
    gun.bloodKills = kills
    gun.bloodSelfDamage = self_damage

def calculate_bounce_vars(gun):
    # TODO: flesh this out
    gun.bounceRange = random.randint(4,5)

def append_gimmick(gun, lst, val):
    if val not in gun.gimmicks:
        lst.append(val)
    return lst

def append_gimmicks(gun, lst, vals):
    for val in vals:
        if val not in gun.gimmicks:
            lst.append(val)
    return lst

def generate_name(gun):
    adjectives = [
        'Bodacious',
        'Horrifying',
        'Unending',
        'Disgusting',
        'Ultra',
        'Tactical',
        'Teething',
        'Bile',
        'Royal',
        'Business',
        'Acidic',
        'Regicidal',
        'Ritualistic',
        'Filthy',
        'Neon',
        'Spiky'
    ]

    nouns = ["Error with noun generator lol"]

    match gun.type:
        case 'MG':
            nouns = [
                "Tommy gun",
                "Repeater",
                "Gat",
                "Kalashnikov",
                "Pistol"
            ]
        case 'SG':
            nouns = [
                "Shotty",
                "Slugger",
                "Blunderbuss",
                "Breach loader",
                "Scattershot"
            ]
        case 'SN':
            nouns = [
                "Rifle",
                "Carbide",
                "Musket",
                "Arquebus",
                "Smoothborne"
            ]
        case 'EX':
            nouns = [
                "Cannon",
                "Missile",
                "Fieldpiece",
                "Artillery",
                "Launcher",
                "Howitzer",
                "Culverin"
            ]

    gun.name = random.choice(adjectives) + " " + random.choice(nouns)


def set_base_stats(gun):
    # Apply base weapon stats per type
    match gun.type:
        case 'MG':
            gun.fireRate = 3
        case 'SG':
            gun.maxRange = 2
            gun.dpt *= 1.1
        case 'SN':
            gun.rangeBonus = 2
            match random.randint(1, 3):
                case 1:
                    gun.gimmicks.append('homing')
                    gun.dpt *= 0.8
                case 2:
                    gun.gimmicks.append('piercing')
                    gun.dpt *= 0.8
                case 3:
                    gun.rangeBonus += 1
                    gun.dpt *= 1.1
        case 'EX':
            gun.minRange = 2
            gun.rangeBonus = 2
            gun.explosionSize = 1
            gun.dpt *= .75

def redeem_tweaks(gun):
    num_tweaks = 1
    num_tweak_rolls = min((gun.gp // 20) + 1,50)
    for i in range(num_tweak_rolls):
        if random.randint(0, 1) == 1:
            num_tweaks += 1

    for i in range(num_tweaks):
        # figure out which tweaks are valid
        # must be recalculated each tweak
        tweaks = []
        match gun.type:
            case 'MG':
                tweaks = ['range 1', 'dpt 1.1']
                if gun.fireRate < 5:
                    tweaks.append('fire rate 1')
            case 'SG':
                tweaks = ['max range 1']
                if gun.fireRate < 3:
                    tweaks.append('fire rate 1')
                if gun.maxRange > 1:
                    tweaks.append('max range -1')
            case 'SN':
                tweaks = ['range 2', 'dpt 1.1']
                if gun.fireRate < 3:
                    tweaks.append('fire rate 1')
            case 'EX':
                tweaks = ['min range 1']
                if gun.explosionSize > 0:
                    tweaks.append('explosion small')
                if gun.explosionSize < 3:
                    tweaks.append('explosion big')
                if gun.fireRate < 3:
                    tweaks.append('fire rate 1')

        # roll tweak
        tweak = random.choice(tweaks)

        # apply tweak
        gun.tweaks.append(tweak)
        match tweak:
            case 'range 1':
                gun.rangeBonus += 1
            case 'range 2':
                gun.rangeBonus += 2
            case 'fire rate 1':
                gun.fireRate += 1
                if gun.type != 'MG':
                    gun.dpt *= 0.95
            case 'dpt 1.1':
                gun.dpt *= 1.1
            case 'max range 1':
                gun.maxRange += 1
            case 'max range -1':
                gun.maxRange -= 1
                gun.dpt *= 1.2
            case 'min range 1':
                gun.rangeBonus += 2
                gun.minRange += 1
            case 'explosion small':
                gun.explosionSize -= 1
                gun.dpt *= 1.1
                gun.minRange -= 1
            case 'explosion big':
                gun.explosionSize += 1
                gun.minRange += 1


def redeem_gimmicks(gun):
    temp = round((gun.gp + 30) / 2)
    rand = random.randint(0, temp) + random.randint(0, temp)
    num_gimmicks = rand // 40

    for i in range(num_gimmicks):
        # figure out which gimmicks are valid
        # must be recalculated each loop
        valid_gimmicks = []
        valid_gimmicks = append_gimmicks(gun, valid_gimmicks, ['fire', 'homing'])
        if gun.type == 'MG':
            valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'low fire rate')
        else:
            valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'high fire rate')
        if gun.type == 'SN':
            valid_gimmicks = append_gimmicks(gun, valid_gimmicks, ['big game hunter', 'bounce'])
        if gun.type == 'SN' or type == 'MG':
            valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'piercing')
        if gun.type == 'EX':
            valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'nuclear')
        if gun.gp > 20:
            valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'blood')
        if gun.gp > 30:
            valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'soul eater')
        if gun.gp > 50:
            if gun.type != 'MG':
                valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'push')
            if 'soul eater' in gun.gimmicks:
                valid_gimmicks = append_gimmick(gun, valid_gimmicks, 'super soul')

        if not valid_gimmicks:
            # no valid gimmicks!
            break

        gimmick = random.choice(valid_gimmicks)
        gun.gimmicks.append(gimmick)

        # actually apply gimmick affects to base stats
        match gimmick:
            case 'fire':
                gun.dpt *= 0.42
            case 'homing':
                gun.dpt *= 0.8
                if gun.type != 'SG':
                    gun.rangeBonus += 2
                else:
                    gun.maxRange += 2
            case 'high fire rate':
                gun.fireRate += 2
                gun.dpt *= 0.9
            case 'low fire rate':
                gun.fireRate -= 2
                gun.dpt *= 1.2
            case 'big game hunter':
                gun.dpt *= 1.2
                gun.rangeBonus += 2
            case 'bounce':
                gun.dpt *= 0.75
                gun.rangeBonus -= 1
                calculate_bounce_vars(gun)
            case 'piercing':
                gun.dpt *= 0.8
                gun.rangeBonus += 2
            case 'nuclear':
                gun.explosionSize += 2
                if gun.explosionSize > 4:
                    gun.explosionSize = 4
                gun.dpt *= 1.1
            case 'blood':
                gun.dpt *= 1.4
                calculate_blood_vars(gun)
            case 'soul eater':
                gun.dpt *= 0.35
        # super soul and push do not affect base stats and are excluded

def calculate_damage_vars(gun):
    target_dps = gun.dpt / gun.fireRate
    lower_bound = max(target_dps * 0.85, target_dps - 15)
    upper_bound = min(target_dps * 1.15, target_dps + 15)
    solutions = []

    for x in range(round(target_dps) + 1):
        min_y = ceil(lower_bound / (3.5 + x))  # Solve for smallest y
        max_y = floor(upper_bound / (3.5 + x))  # Solve for largest y

        if min_y <= max_y:  # Only consider valid ranges
            for y in range(min_y, max_y + 1):
                solutions.append((x, y))

    if not solutions:
        print('no valid damage numbers found!')
        return
    number_solutions = len(solutions)
    if number_solutions % 2 == 0:
        # it splits evenly
        solution_index = random.randint(0,int(number_solutions/2)) + random.randint(0,int(number_solutions/2))
    else:
        #one smaller, one larger num
        smol = floor(number_solutions/2)
        beeg = ceil(number_solutions/2)
        solution_index = random.randint(0, smol) + random.randint(0, beeg)
    # TODO: this is out of bounds sometimes, fix
    solution = solutions[solution_index]
    gun.plusDmg = solution[0]
    gun.timesDmg = solution[1]



class Gun:
    def __init__(self, zp_arg, type_arg):
        self.ZP = zp_arg
        self.gp = max(3,self.ZP + random.randint(-4,4))
        self.dpt = (0.010387 * self.gp * self.gp) + 10.60839

        # init vars
        self.fireRate = 1
        self.rangeBonus = 0
        self.plusDmg = 0
        self.timesDmg = 1
        self.minRange = 0
        self.maxRange = 9999
        self.explosionSize = -1
        self.tweaks = []
        self.gimmicks = []

        self.bloodKills = 0
        self.bloodSelfDamage = 0

        self.bounceRange = 0

        self.name = ""

        # init type
        types = ['MG', 'SG', 'SN', 'EX']
        if type_arg is None:
            self.type = random.choice(types)
        else:
            self.type = type_arg

        set_base_stats(self)
        redeem_tweaks(self)
        redeem_gimmicks(self)
        calculate_damage_vars(self)
        generate_name(self)

    def display(self):
        dont_print_these_gimmicks = [
            'nuclear',
            'high fire rate',
            'low fire rate',
            'big game hunter',
            ''
        ]

        print (f'{self.name} - {self.type} - ${self.gp}')
        print(f'Fire Rate: {self.fireRate}')
        # range stuff
        if self.type == 'SG':
            print(f'Max Range: {self.maxRange}')
        else:
            if self.rangeBonus > 0:
                print(f'+{self.rangeBonus} Range')
            elif self.rangeBonus < 0:
                print(f'{self.rangeBonus} Range')
            if self.type == 'EX':
                print(f'Min Range: {self.minRange}')
        # dmg stuff
        if self.plusDmg > 0 and self.timesDmg > 1:
            print(f'+{self.plusDmg} dmg, x{self.timesDmg} dmg')
        elif self.plusDmg > 0:
            print(f'+{self.plusDmg} dmg')
        elif self.timesDmg > 1:
            print(f'x{self.timesDmg} dmg')
        # gimmicks and whatnot
        for gimmick in self.gimmicks:
            if gimmick not in dont_print_these_gimmicks:
                if gimmick == 'blood':
                    print(f'[blood] - {self.bloodKills} kills, {self.bloodSelfDamage} self damage penalty')
                elif gimmick == 'bounce':
                    print(f'bounce - {self.bounceRange} bounce range')
                elif gimmick == 'soul eater':
                    if 'super soul' not in self.gimmicks:
                        print(f'[{gimmick}]')
                elif gimmick == 'super soul':
                    print('[soul eater] - also gain 2 spaces of movement on kill')
                else:
                    print(f'[{gimmick}]')
        if self.type == 'EX':
            print(f'Explosion size: {self.explosionSize}')

        # avg dmg vals
        min_dmg = (1 + self.plusDmg) * self.timesDmg * self.fireRate
        avg_dmg = (3.5 + self.plusDmg) * self.timesDmg * self.fireRate
        max_dmg = (6 + self.plusDmg) * self.timesDmg * self.fireRate
        print(f'{min_dmg} / {avg_dmg} / {max_dmg}')

    def display_all(self):
        print(self.name)
        print(f'ZP: {self.ZP}, GP: {self.gp}, type: {self.type}')
        print(f'tweaks: {self.tweaks}')
        print(f'gimmicks: {self.gimmicks}')
        print(f'dpt: {self.dpt}, fire rate: {self.fireRate}, range: {self.rangeBonus}')
        print(f'+{self.plusDmg} dmg, x{self.timesDmg} dmg')
        minDmg = (1 + self.plusDmg) * self.timesDmg * self.fireRate
        avgDmg = (3.5 + self.plusDmg) * self.timesDmg * self.fireRate
        maxDmg = (6 + self.plusDmg) * self.timesDmg * self.fireRate
        print(f'{minDmg} / {avgDmg} / {maxDmg}')
        if self.type == 'SG':
            print(f'max range: {self.maxRange}')
        if self.type == 'EX':
            print(f'min range: {self.minRange}, explosion size: {self.explosionSize}')
        if 'bounce' in self.gimmicks:
            print(f'bounce range: {self.bounceRange}')
        if 'blood' in self.gimmicks:
            print(f'kills: {self.bloodKills}, self dmg: {self.bloodSelfDamage}')

    # fires 1 shot at an enemy y distance away
    def shoot(self, enemy_distance):
        if enemy_distance > self.maxRange:
            print('This enemy is too far away to shoot!')
            return
        if enemy_distance < self.minRange:
            print('This enemy is too close to shoot!')
            return
        final_distance = max(0, enemy_distance - self.rangeBonus)
        roll = random.randint(1,6)
        if self.type != 'SG':
            base_dmg = roll - final_distance
        else:
            base_dmg = roll
        if base_dmg <= 0:
            print(f'Rolled a {roll} - Miss!')
        else:
            final_dmg = (base_dmg + self.plusDmg) * self.timesDmg
            print(f'Rolled a {roll} - Hit for {final_dmg} Damage!')

    def pepper(self, enemy_distance, num_shots):
        print('------------')
        print(f'Shooting the {self.name} {num_shots} times at an enemy {enemy_distance} spaces away...')
        for i in range(num_shots):
            self.shoot(enemy_distance)

    # fires all shots of a gun into one enemy x distance away
    def unload(self, enemy_distance):
        print('------------')
        print(f'Unloading the {self.name} at an enemy {enemy_distance} spaces away...')
        for i in range(self.fireRate):
            self.shoot(enemy_distance)

if __name__ == '__main__':
    gun_test = Gun(10, None)
    gun_test.display()
    gun_test.unload(3)

    # TODO: scanner w commands
    # there is a gun list saved across commands
    # generate(num guns, zp), adds to gun list
    # get stats on gun n from list
    # dump list (shows all guns on list by calling above function)
    # get gimmicks on gun n, get tweaks on gun n, etc.
    # clear gun list
    # rm gun n
    # undo deletion?
    # buy gun - move it to seperate list
    # roll gun n
    # same commands on inventory