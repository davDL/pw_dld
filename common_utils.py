def get_color_by_index(index):
    if index % 5 == 0:
        return "#f44236"
    elif index % 4 == 0:
        return "#54ca67"
    elif index % 3 == 0:
        return "#6777ef"
    elif index % 2 == 0:
        return "#fba425"
    else:
        return "#365185"

def get_total_page(page_size, total_data):
  data_div_page_size = total_data // page_size
  data_mod_page_size = total_data % page_size
  total_page = data_div_page_size if data_mod_page_size == 0 else (data_div_page_size + 1)

  return total_page