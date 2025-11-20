import pandas as pd

# Read Excel file
idc = pd.read_excel("IDC_Collections_list.xlsx")

# Get the first column as a list
idc = idc.iloc[:, 0].tolist()


# Read Excel file
tcia = pd.read_excel("TCIA_data_full.xlsx")

# Get the first column as a list


tcia = tcia.iloc[:, 0].tolist()


result = list(set(idc) - set(tcia))


# print(idc)
# print()
# print(tcia)
# print()
# print(*result, sep="\n")

# print()
# result2 = list(set(tcia) - set(idc))
# print(*result2, sep="\n")



# print()
# result3 = list(set(tcia) & set(idc))
# print(*result3, sep="\n")


print(len(idc))
