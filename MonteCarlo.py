from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import math
import os
import numpy as np
import ctypes


def MonteCarlo_Simulation(S, V, T, N, mu=0):
    '''
    --------------
    |   Intput   |
    --------------

    1. Stock Price
    2. Volatility
    3. Time
    4. Period
    5. Expected Return (Default as zero)

    --------------
    |   Output   |
    --------------

    1. Final Stock Price
    2. Simulation Process Price
    '''

    stock_price = S
    delta_t = T / N
    simulation_process = [S]

    for _ in range(N):

        epsilon = np.random.standard_normal()

        stock_price_change = mu*delta_t*stock_price + V*epsilon*np.sqrt(delta_t)*stock_price
        stock_price = stock_price + stock_price_change
        simulation_process.append(stock_price)

    return stock_price, simulation_process


def Simulate():

    global result_image
    global canvas

    try:

        # ------------------------------------ #
        #    Exception 1. Input Data Type      #
        # ------------------------------------ #
        option_type = option_type_entry.get()

        if option_type not in ['C', 'c', 'P', 'p']:
            raise ValueError(f'{option_type} Option Type')

        S = float(stock_price_entry.get())
        K = float(strike_price_entry.get())
        T = float(time_entry.get())
        R = float(rate_entry.get())
        V = float(volatility_entry.get())
        N = int(period_entry.get())
        how_many_times = int(simulate_times_entry.get())

        result_option_value = []
        result_simulation_process_result = []
        for i in range(how_many_times):

            result = MonteCarlo_Simulation(S, V, T, N)
            stock_price_T = result[0]
            option_value_T = max(stock_price_T - K, 0) if option_type == 'C' \
                else max(K - stock_price_T, 0)
            result_option_value.append(option_value_T)

            if len(result_simulation_process_result) != 10:

                result_simulation_process_result.append(result[1])

            else:
                pass

        expected_option_price = sum(result_option_value) / how_many_times
        pv_of_expected_option_price = expected_option_price * math.exp(-R*T)

        # -------------------- #
        #        Plot          #
        # -------------------- #
        plt.style.use('bmh')
        result_simulation_process_result = list(
            map(list, zip(*result_simulation_process_result))
        )
        fig = plt.figure(figsize=(8, 5))

        ax = fig.add_subplot()

        fig.suptitle("Option Price (PV): " + r"$\bf{" +
                     '{:.2f}'.format(pv_of_expected_option_price) + "}$  " +
                     "Simulation Times: " + r"$\bf{" + str(how_many_times) + "}$", fontsize=18)

        ax.axhline(y=S, color="k", ls="--", alpha=0.8)

        plt.plot(result_simulation_process_result)
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)

        plt.xlim(left=0)
        plt.xlim(right=N)
        plt.xticks(np.arange(0, N, int(N/10)))

        plt.savefig('result.png', dpi=300)

        canvas_width = 600
        canvas_height = 400
        canvas = Canvas(result_frame, width=canvas_width,
                        height=canvas_height, bg=bg_color
                        )
        canvas.grid(row=1, column=0, rowspan=10)
        result_image = Image.open('result.png')
        result_image = result_image.resize(
            (canvas_width + 40, canvas_height-20),
            Image.ANTIALIAS
        )
        result_image = ImageTk.PhotoImage(result_image)
        canvas.create_image((canvas_width/2 + 20, canvas_height/2 + 20), image=result_image, anchor="center")  # row=0, column=0, image=result_image)
        os.system('del result.png')

    except ValueError as e:

        error_message = str(e)
        error_loc = error_message.find(':')
        wrong_input = error_message[error_loc+1:]

        if len(error_message[error_loc+1:].strip()) != 0:
            messagebox.showinfo(f'Input Wrong', f'{wrong_input} is invalid.')

        else:
            wrong_input = 'blank input'
            messagebox.showinfo(f'Input Wrong', f'{wrong_input} is invalid.')

    except ZeroDivisionError as e:

        messagebox.showinfo("Input Wrong", "Set Period(N) more than 10")
        print(e)

    except Exception as e:

        messagebox.showinfo("Unknown Error", "Please Contact ycy.tai@gmail.com")
        print(e)


def Reset():

    canvas.destroy()

    option_type_entry.delete(0, END)
    stock_price_entry.delete(0, END)
    strike_price_entry.delete(0, END)
    time_entry.delete(0, END)
    rate_entry.delete(0, END)
    volatility_entry.delete(0, END)
    period_entry.delete(0, END)
    simulate_times_entry.delete(0, END)


title = '  Monte Carlo Simulation'
bg_color = 'white'
font_type = 'Tw Cen MT'

root = Tk()
root.title('Financial Engineering')
root.iconbitmap('bars.ico')
root.geometry('960x420')
root.configure(bg=bg_color)
root.resizable(height='False', width='False')

# ---------------------- #
#         Frame          #
# ---------------------- #
main_frame = Frame(root, width=360, height=420, relief='groove', borderwidth=2, bg='#c6c9cf')
result_frame = Frame(root, width=600, height=420, relief='groove', borderwidth=2, bg=bg_color)


main_frame.pack(side='left', fill='both', expand=True)
result_frame.pack(side='right', fill='both', expand=True)


# ---------------------- #
#         Label          #
# ---------------------- #
label_font = (font_type, 16)
label_color = '#c6c9cf'

title_label = Label(main_frame, font=(font_type, 20, 'bold'), fg='#1c5a9c', bg=label_color, text=title, justify='center')
option_type_labeL = Label(main_frame, font=label_font, bg=label_color, text='Option Type (C/P)')
stock_price_label = Label(main_frame, font=label_font, bg=label_color, text='Stock Price (S)')
strike_price_label = Label(main_frame, font=label_font, bg=label_color, text='Strike Price (K)')
time_label = Label(main_frame, font=label_font, bg=label_color, text='Year (T)')
rate_label = Label(main_frame, font=label_font, bg=label_color, text='Rate (R)')
volatility_label = Label(main_frame, font=label_font, bg=label_color, text='Volatility (V)')
period_label = Label(main_frame, font=label_font, bg=label_color, text='Period (N)')
simulate_times_label = Label(main_frame, font=label_font, bg=label_color, text='Simlation (M)')


title_label.grid(row=0, column=0, padx=4, pady=4,  columnspan=2)
option_type_labeL.grid(row=1, column=0, padx=4, pady=4, sticky='e')
stock_price_label.grid(row=2, column=0, padx=4, pady=4, sticky='e')
strike_price_label.grid(row=3, column=0, padx=4, pady=4, sticky='e')
time_label.grid(row=4, column=0, padx=4, pady=4, sticky='e')
rate_label.grid(row=5, column=0, padx=4, pady=4, sticky='e')
volatility_label.grid(row=6, column=0, padx=4, pady=4, sticky='e')
period_label.grid(row=7, column=0, padx=4, pady=4, sticky='e')
simulate_times_label.grid(row=8, column=0, padx=4, pady=4, sticky='e')


# ---------------------- #
#         Entry          #
# ---------------------- #
entry_width = 12
entry_font = (font_type, 16)
entry_color = '#e4e7ed'

option_type_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)
stock_price_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)
strike_price_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)
time_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)
rate_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)
volatility_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)
period_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)
simulate_times_entry = Entry(main_frame, width=entry_width, font=entry_font, relief='groove', justify='center', borderwidth=2, bg=entry_color)


option_type_entry.grid(row=1, column=1, padx=4, pady=5)
stock_price_entry.grid(row=2, column=1, padx=4, pady=5)
strike_price_entry.grid(row=3, column=1, padx=4, pady=5)
time_entry.grid(row=4, column=1, padx=4, pady=5)
rate_entry.grid(row=5, column=1, padx=4, pady=5)
volatility_entry.grid(row=6, column=1, padx=4, pady=5)
period_entry.grid(row=7, column=1, padx=4, pady=5)
simulate_times_entry.grid(row=8, column=1, padx=4, pady=5)


# ----------------------- #
#         Button          #
# ----------------------- #
simulate_button = Button(
    main_frame, bg='#bed4eb', text='Simulate',
    padx=4, pady=1, width=6,
    relief='groove', font=(font_type, 14), command=Simulate
)

reset_button = Button(
    main_frame, bg='#fca4a4', text='Reset',
    padx=4, pady=1, width=6,
    relief='groove', font=(font_type, 14), command=Reset
)

simulate_button.grid(row=9, column=1)
reset_button.grid(row=9, column=0)

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/200)
root.mainloop()
