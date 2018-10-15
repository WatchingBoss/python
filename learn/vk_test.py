#!/usr/bin/env python3
"""
Get user first and last name in vk.com
"""

import vk_requests
import openpyxl


def define_workbook():
    work_book = openpyxl.Workbook()
    sheet = work_book.active
    sheet.title = "VK users"
    sheet['A1'] = "ID"
    sheet['B1'] = "First name"
    sheet['C1'] = "Last name"
    return work_book, sheet


def set_value_and_width(sheet, letter, row, column, string):
    sheet.cell(row=row, column=column).value = string
    if not sheet.column_dimensions[letter].width or \
       sheet.column_dimensions[letter].width < len(str(string)):
        sheet.column_dimensions[letter].width = len(str(string)) + 4


def store_in_spread_sheet(sheet, row, user_id, user_fn, user_ln):
    set_value_and_width(sheet, 'A', row, 1, user_id)
    set_value_and_width(sheet, 'B', row, 2, user_fn)
    set_value_and_width(sheet, 'C', row, 3, user_ln)


def print_to_console(user_id, user_fn, user_ln):
    print("ID: {:8} First name: {:15} Last name: {}".format(user_id, user_fn, user_ln))


def get_info(sheet, row, api, user_id):
    user = api.users.get(user_ids=user_id)[0]
    if user["first_name"] != "DELETED":
        store_in_spread_sheet(sheet, row, user["id"], user["first_name"], user["last_name"])
        print_to_console(user["id"], user["first_name"], user["last_name"])
        return 1
    return 0


def start():
    api = vk_requests.create_api(app_id=6480738, service_token="31cc5d6031cc5d6031cc5d604e31\
aebe02331cc31cc5d606b3059678598a91622bc33d3")
    work_book, sheet = define_workbook()

    row = 2
    for user_id in range(1, 100):
        if get_info(sheet, row, api, user_id):
            row += 1

    work_book.save("vk_api.xlsx")


if __name__ == "__main__":
    start()
