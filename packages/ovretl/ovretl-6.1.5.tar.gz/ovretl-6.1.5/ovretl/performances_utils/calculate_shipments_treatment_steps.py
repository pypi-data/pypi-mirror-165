import pandas as pd


def drop_not_arrived_shipment_groups(shipment_events_df: pd.DataFrame):
    shipment_events_df = shipment_events_df.sort_values(by=["date"], ascending=False).reset_index(drop=True)
    if shipment_events_df.loc[0, "date_type"] == "estimated":
        return False
    return True


def extract_arrived_date_from_events(events_shipment_df: pd.DataFrame):
    events_shipment_df = events_shipment_df.dropna(subset=["shipment_id", "date"], how="any").drop(
        ["created_at"], axis=1
    )
    events_shipment_df = events_shipment_df.groupby("shipment_id").filter(drop_not_arrived_shipment_groups)
    events_shipment_df = events_shipment_df.sort_values(by=["shipment_id", "date"], ascending=False)
    events_shipment_df = events_shipment_df.drop_duplicates(subset=["shipment_id"])
    events_shipment_df.loc[:, "header"] = "shipment_arrived"
    events_shipment_df = events_shipment_df.rename(columns={"date": "created_at"})
    return events_shipment_df[["created_at", "header", "shipment_id"]]


def extract_finished_date_from_shipments(shipments_df: pd.DataFrame):
    shipments_df = shipments_df.dropna(subset=["finished_date"]).drop(["created_at"], axis=1)
    shipments_df.loc[:, "header"] = "shipment_finished"
    shipments_df = shipments_df.rename(columns={"finished_date": "created_at", "id": "shipment_id"})
    return shipments_df[["created_at", "header", "shipment_id"]]


def concatenate_activities(
    events_shipment_df: pd.DataFrame, activities_clean_df: pd.DataFrame, shipments_df: pd.DataFrame,
):
    activities_clean_df = pd.concat([activities_clean_df, events_shipment_df, shipments_df], sort=False)
    activities_clean_df.loc[:, "created_at"] = pd.to_datetime(activities_clean_df["created_at"]).apply(
        lambda t: t.replace(tzinfo=None)
    )
    activities_clean_df = activities_clean_df.sort_values(by=["shipment_id", "header", "created_at"], ascending=True)
    activities_clean_df = activities_clean_df.drop_duplicates(subset=["shipment_id", "header"])

    activities_clean_df = activities_clean_df[
        activities_clean_df["header"].isin(
            [
                'quotation_asked',
                'request_considered',
                'quotation_purchase_ready',
                'propositions_received',
                'quotation_accepted',
                'shipment_booked',
                'shipment_arrived',
                'shipment_finished',
                'billing_available',
                'billing_paid',
            ]
        )
    ]
    activities_clean_df = pd.pivot_table(
        activities_clean_df, values="created_at", index=["shipment_id"], columns=["header"], aggfunc="first",
    )
    return activities_clean_df.reset_index()


def calculate_shipments_treatment_steps(
    events_shipment_df: pd.DataFrame, activities_clean_df: pd.DataFrame, shipments_df: pd.DataFrame,
):
    events_shipment_df = extract_arrived_date_from_events(events_shipment_df=events_shipment_df)
    activities_clean_df = activities_clean_df.dropna(subset=["shipment_id"])[
        ["created_at", "header", "shipment_id", "employee_id"]
    ]
    shipments_df = extract_finished_date_from_shipments(shipments_df=shipments_df)

    activities_clean_df = concatenate_activities(
        events_shipment_df=events_shipment_df, activities_clean_df=activities_clean_df, shipments_df=shipments_df,
    )
    return activities_clean_df.drop(["employee_id"], axis=1, errors="ignore")
