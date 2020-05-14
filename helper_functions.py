from IPython.display import clear_output
import seaborn as sns
import pandas as pd
import os
import moviepy.editor as mpy


def update_progress(progress):
    """progress bar"""
    bar_length = 20
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1

    block = int(round(bar_length * progress))

    clear_output(wait = True)
    text = "Creating Plots: [{0}] {1:.1f}%".format( "#" * block + "-" * (bar_length - block), progress * 100)
    print(text)

def collect_data(people):
    """collect data to be plotted"""
    list_of_people = people.copy()
    healthy_population = healthy_people(list_of_people)
    infected_population = infected_people(list_of_people)
    immune_population = immune_people(list_of_people)


    num_healthy = len(healthy_population)
    num_infected = len(infected_population)
    num_immune = len(immune_population)

    x_positions = [person.get_x() for person in people]
    y_positions = [person.get_y() for person in people]
    status = [person.get_status() for person in people]
    return num_healthy, num_infected, num_immune, x_positions, y_positions, status


def healthy_people(list_of_people):
    """returns a list of healthy people"""
    healthy_people = []
    for person in list_of_people:
        if person.status == "naive":
            healthy_people.append(person)
    return healthy_people

def infected_people(list_of_people):
    """returns a list of infected people"""
    infected_people = []
    for person in list_of_people:
        if person.status == "infected":
            infected_people.append(person)
    return infected_people

def immune_people(list_of_people):
    """returns a list of immune people"""
    immune_people = []
    for person in list_of_people:
        if person.status == "immune":
            immune_people.append(person)
    return immune_people


def make_plots(df_infections, df_positions, last_day):
    """Make the plots and gif given the data from each day"""
    os.system("rm -rf plots")
    os.mkdir("plots")
    print("Generating Plots")
    for day in range(0, min(365, last_day)):
        sns.scatterplot(data = df_positions[df_positions["day"] == day], x = "x_position", y = "y_position", hue = "status", hue_order = ["naive", "infected", "immune"])
        frame1 = plt.gca()
        for xlabel_i in frame1.axes.get_xticklabels():
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
        for xlabel_i in frame1.axes.get_yticklabels():
            xlabel_i.set_fontsize(0.0)
            xlabel_i.set_visible(False)
        for tick in frame1.axes.get_xticklines():
            tick.set_visible(False)
        for tick in frame1.axes.get_yticklines():
            tick.set_visible(False)
        plt.xlabel("")
        plt.ylabel("")
        num_infected = df_infections[df_infections["days"] == day].infected.iloc[0]
        plt.title(f"Day: {day}")
        plt.legend(loc=1)
        plt.savefig(f"plots/day_{day}.png", dpi = 100)
        plt.savefig(f"plots/day_{day}.pdf")
        plt.clf()
        update_progress(day / min(365, last_day))


    gif_name = 'infections'
    fps = 8
    file_list = glob.glob('plots/*.png') # Get all the pngs in the current directory
    list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('{}.gif'.format(gif_name), fps=fps)

    sns.scatterplot(data = df_infections, x = "days", y = "infected", label = "infected")
    sns.scatterplot(data = df_infections, x = "days", y = "healthy", label = "naive")
    sns.scatterplot(data = df_infections, x = "days", y = "immune", label = "immune")
    plt.legend()
    plt.ylabel("People")
    plt.xlabel("Days")
    plt.savefig("infections_over_time.png")
    plt.show()

    return Image("infections.gif")
