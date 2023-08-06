def print_progressbar(iteration,
                      total,
                      prefix='',
                      suffix='',
                      decimals=1,
                      length=100,
                      fill='█',
                      print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)

    Author:
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r\t{prefix} |{bar}| {percent}% {suffix}', end=print_end, flush=True)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":
    # Initial call to print 0% progress
    import time
    totals = 100
    print_progressbar(0, totals, prefix='Progress:', suffix='Complete', length=50)
    for i in range(totals):
        # Do stuff...
        time.sleep(0.05)
        # Update Progress Bar
        print_progressbar(i + 1, totals, prefix='Progress:', suffix='Complete', length=50)
