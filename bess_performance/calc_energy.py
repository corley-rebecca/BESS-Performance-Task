import pandas as pd

#assumed 15 min intervals (0.25)
def calculate_daily_energy(df, dc_columns, file_column='source_file', interval_hours=0.25):

    # dictionary
    daily_energy = {}
    # Loop over each DC input column
    for col in dc_columns:
        # power (kW) * interval (hours) = energy per row (kWh)
        energy = df[col] * interval_hours
        #define charging (-) and discharging (+)
        charged = energy[energy < 0].abs()  # charging is negative (take abs val), electrons flowing in
        discharged = energy[energy > 0]     # discharging is positive, electrons flowing out

         # sum the energy per file/day
        daily_charged = charged.groupby(df[file_column]).sum()
        daily_discharged = discharged.groupby(df[file_column]).sum()

        # store results in dictionary
        daily_energy[col] = pd.DataFrame({
            'charged_kWh': daily_charged,
            'discharged_kWh': daily_discharged
        })

    # Combine all columns into one DataFrame
    result = pd.concat(daily_energy, axis=1)

    return result
