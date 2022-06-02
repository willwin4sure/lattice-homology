import xlsxwriter
from math import ceil
import find_d_invariant

p = (int)(input("p:"))
q = (int)(input("q:"))
r = (int)(input("r:"))

workbook = xlsxwriter.Workbook('sheet for ' + str(p) + ', ' + str(q) + ', ' + str(r) + '.xlsx')
worksheet = workbook.add_worksheet('sheet')
format_one_bold = workbook.add_format(properties={'bg_color': 'lime', 'bold': True})
format_one = workbook.add_format(properties={'bg_color': 'lime'})
format_two = workbook.add_format(properties={'bg_color': 'green'})
format_two_bold = workbook.add_format(properties={'bg_color': 'green', 'bold': True})
format_neg_one = workbook.add_format(properties={'bg_color': 'pink'})
format_neg_one_bold = workbook.add_format(properties={'bg_color': 'pink', 'bold': True})
format_neg_two = workbook.add_format(properties={'bg_color': 'red'})
format_neg_two_bold = workbook.add_format(properties={'bg_color': 'red', 'bold': True})
format_zero_bold = workbook.add_format(properties={'bold': True})

naught = p*q*r-p*q-p*r-q*r


def find_delta(p,q,r,n):
    consts = find_d_invariant.find_constants(p,q,r)
    return 1 - consts[0] * n - ceil((n*consts[1])/p) - ceil((n*consts[2])/q) - ceil((n*consts[3])/r)

delta_list = []

for i in range(((int)(naught/(p*q)) + 1)*p*q + 1):
    delta_list.append(find_delta(p,q,r,i))

rowsums = []
for i in range(((int)(naught/(p*q))) + 1):
    sum = 0
    for j in range(p*q):
        sum += delta_list[i*p*q+j]
    rowsums.append(sum)

for i in range((int)((naught/(p*q))) + 1):
    for j in range(p*q):
        if rowsums[i] >= 0:
            if delta_list[i * p * q + j] == 1:
                worksheet.write(i, j, i * p * q + j, format_one)
            if delta_list[i * p * q + j] == 2:
                worksheet.write(i, j, i * p * q + j, format_two)
            if delta_list[i * p * q + j] == 0:
                worksheet.write(i, j, i * p * q + j)
            if delta_list[i * p * q + j] == -1:
                worksheet.write(i, j, i * p * q + j, format_neg_one)
            if delta_list[i * p * q + j] == -2:
                worksheet.write(i, j, i * p * q + j, format_neg_two)
        else:
            if delta_list[i * p * q + j] == 1:
                worksheet.write(i, j, i * p * q + j, format_one_bold)
            if delta_list[i * p * q + j] == 2:
                worksheet.write(i, j, i * p * q + j, format_two_bold)
            if delta_list[i * p * q + j] == 0:
                worksheet.write(i, j, i * p * q + j, format_zero_bold)
            if delta_list[i * p * q + j] == -1:
                worksheet.write(i, j, i * p * q + j, format_neg_one_bold)
            if delta_list[i * p * q + j] == -2:
                worksheet.write(i, j, i * p * q + j, format_neg_two_bold)

workbook.close()
