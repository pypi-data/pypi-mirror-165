""""# Define base url
        base_url = "https://curia.europa.eu/juris/liste.jsf?formId=caseLawSearchForm&lang=en&jur=CJ,GC,CST,CJEU&num="
        # Define empty data frame
        df = pd.DataFrame()
        # Loop over lists of cases
        for case_list in case_lists:
            # Define url
            url = base_url + case_list
            # Scrape data
            data = pd.read_html(url, header = 0)[0]
            # Append data to data frame
            df = df.append(data, ignore_index = True)
        # Rename columns
        df.columns = ["case_id", "case_info"]
        # Extract CELEX identifiers from hyperlinks
        df["celex"] = df["case_id"].str.extract(r"([A-Z]{2}\d{4}\d{2}\w{1}\d{3})")
        # Parse references to cases and appeals
        if parse:
            df["case"] = df["case_info"].str.extract(
                r"Case ([A-Z]{2}\d{4}\d{2}\w{1}\d{3})"
            )
            df["appeal"] = df["case_info"].str.extract(
                r"Appeal ([A-Z]{2}\d{4}\d{2}\w{1}\d{3})"
            )
        # Return data frame
        return df"""
