from pathlib import Path
import pandas as pd
from collections import defaultdict


def bus_statistics(directory):
    # Root directory containing Process_* folders
    root_dir = Path(directory)

    # Tracking dictionaries
    outage_count = defaultdict(int)        # nonzero outage hours
    outage_magnitude = defaultdict(float)  # total outage magnitude

    # Find all outage record files
    files = (
        list(root_dir.glob("Process_*/Sample_*/Outage_Records_Sample_*.xlsx"))
        or list(root_dir.glob("Sample_*/Outage_Records_Sample_*.xlsx"))
    )

    for file in files:
        try:
            # Read sheet
            df = pd.read_excel(
                file,
                sheet_name="loadcurt_bus",
                index_col=0
            )

            # Ensure numeric
            df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

            # Loop through buses (rows)
            for bus in df.index:
                vals = df.loc[bus]

                # Count hours with outage
                nonzero = (vals != 0)
                outage_count[bus] += nonzero.sum()

                # Sum outage magnitude
                outage_magnitude[bus] += vals.sum()

        except Exception as e:
            print(f"Skipping {file}: {e}")

    if not files:
        print("No outages detected to print outage statistics.")
        return
    # ==========================================
    # BUILD SERIES
    # ==========================================
    count_series = pd.Series(outage_count, dtype=float)
    mag_series = pd.Series(outage_magnitude, dtype=float)

    print(count_series)

    # Keep only buses with nonzero outage hours
    valid_buses = count_series[count_series > 0].index

    count_series = count_series.loc[valid_buses]
    mag_series = mag_series.loc[valid_buses]

    # Average outage
    avg_series = mag_series / count_series


    # ==========================================
    # SORT DESCENDING
    # ==========================================
    count_series = count_series.sort_values(ascending=False)
    mag_series   = mag_series.sort_values(ascending=False)
    avg_series   = avg_series.sort_values(ascending=False)


    # ==========================================
    # TOP BUSES
    # ==========================================
    most_freq_bus = count_series.idxmax()
    most_freq_count = count_series.max()

    most_outage_bus = mag_series.idxmax()
    most_outage_mag = mag_series.max()

    highest_avg_bus = avg_series.idxmax()
    highest_avg_outage = avg_series.max()


    # ==========================================
    # WRITE OUTPUT TO TXT
    # ==========================================
    outfile = root_dir / "bus_outage_summary.txt"

    with open(outfile, "w") as f:
        f.write("===================\n")
        f.write("BUS OUTAGE SUMMARY \n")
        f.write("===================\n\n")


        # --------------------------------------
        # 1) OUTAGE FREQUENCY
        # --------------------------------------
        f.write("=== TOTAL OUTAGE HOURS ===\n")
        f.write("Rank\tBus\tHours\n")

        for i, (bus, val) in enumerate(count_series.items(), start=1):
            f.write(f"{i}\t{bus}\t{val}\n")

        f.write("\n")


        # --------------------------------------
        # 2) TOTAL OUTAGE MAGNITUDE
        # --------------------------------------
        f.write("=== TOTAL OUTAGE MAGNITUDE (MW) ===\n")
        f.write("Rank\tBus\tMagnitude\n")

        for i, (bus, val) in enumerate(mag_series.items(), start=1):
            f.write(f"{i}\t{bus}\t{val:.4f}\n")

        f.write("\n")

        # --------------------------------------
        # 3) AVERAGE OUTAGE
        # --------------------------------------
        f.write("=== AVERAGE OUTAGE MAGNITUDE (MW/Hour) ===\n")
        f.write("Rank\tBus\tAverage\n")

        for i, (bus, val) in enumerate(avg_series.items(), start=1):
            f.write(f"{i}\t{bus}\t{val:.4f}\n")

        f.write("\n")


        # --------------------------------------
        # SUMMARY
        # --------------------------------------
        f.write("=== TOP BUSES ===\n")
        f.write(
            f"Most outage hours : "
            f"{most_freq_bus} ({most_freq_count} hours)\n"
        )

        f.write(
            f"Most outage magnitude : "
            f"{most_outage_bus} ({most_outage_mag:.4f})\n"
        )

        f.write(
            f"Highest average outage: "
            f"{highest_avg_bus} ({highest_avg_outage:.4f})\n"
        )


    print(f"Saved summary to: {outfile}")