def map_data_to_scheme_name(data_based_on_scheme_name, excel_df):
    first_col_to_map = []
    scheme_name = ''
    for idx, row in excel_df.iterrows():
        json_format_data = {}
        for ev_idx, col in enumerate(row):
            if idx == 0:
                first_col_to_map.append(col)
            else:
                if col == '-':
                    json_format_data[first_col_to_map[ev_idx]] = None
                else:
                    json_format_data[first_col_to_map[ev_idx]] = col
                if ev_idx == 0:
                   scheme_name = col

            if scheme_name:
                if scheme_name not in data_based_on_scheme_name:
                    data_based_on_scheme_name[scheme_name] = json_format_data
                else:
                    data_based_on_scheme_name[scheme_name].update(json_format_data)
