from Core.HookWindow import LocateImage


def ScanStarving(StatsPositions):
    IsStarving = [0, 0]

    IsStarving[0], IsStarving[1] = LocateImage('images/PlayerStats/Starving.png', Precision=0.9, Region=(
        StatsPositions[0], StatsPositions[1], StatsPositions[2], StatsPositions[3]))
    if IsStarving[0] != 0 and IsStarving[1] != 0:
        return True
    else:
        return False
