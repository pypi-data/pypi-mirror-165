import pandas as pd


def merge_with_shipments_containers_then_with_propositions_containers(
        shipments_df: pd.DataFrame, shipments_containers_df: pd.DataFrame, propositions_containers_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    The former logic implemented used to first merge with propositions containers then with shipments containers.
    Now it is the contrary. We still don't know when the logic has been changed on Tech side, but the Data did this fix
    on Monday, July 18th 2022.
    NB: Most of the time, the shipment's containers info and the shipment's best proposition's containers info are the
    same, but may differ in case an operational has not rigorously updated the proposition after editing the shipment's
    containers. Hence, it is better to rely primarily on the shipment's containers info.
    :param shipments_df:
    :param shipments_containers_df:
    :param propositions_containers_df:
    :return:
    Note:
        Modified date: 18-07-2022
        Author: SB
    """
    shipments_df = pd.merge(
        shipments_df,
        shipments_containers_df[["teus", "tc", "hazardous", "refrigerated", "shipment_id"]],
        how="left",
        on="shipment_id",
    )

    shipments_df_with_teus = shipments_df[~shipments_df["teus"].isnull()]
    shipments_df_without_teus = shipments_df[shipments_df["teus"].isnull()].drop(
        ["teus", "tc", "hazardous", "refrigerated"], axis=1
    )

    shipments_df_without_teus = pd.merge(
        shipments_df_without_teus,
        propositions_containers_df[["teus", "tc", "hazardous", "refrigerated", "proposition_id"]],
        how="left",
        on="proposition_id",
    )
    return (
        pd.concat([shipments_df_with_teus, shipments_df_without_teus], sort=False)
        .reset_index(drop=True)
        .rename(columns={"hazardous": "containers_hazardous", "refrigerated": "containers_refrigerated",})
    )


def split_propositions_shipments_containers(containers_df: pd.DataFrame):
    propositions_containers_df = containers_df[~containers_df["proposition_id"].isnull()]
    shipments_containers_df = containers_df[~containers_df["shipment_id"].isnull()]
    return propositions_containers_df, shipments_containers_df


def merge_shipments_with_containers(
    shipments_df: pd.DataFrame, containers_df: pd.DataFrame, drop_duplicate_key="shipment_id",
):
    (propositions_containers_df, shipments_containers_df,) = split_propositions_shipments_containers(containers_df)
    shipments_df = merge_with_shipments_containers_then_with_propositions_containers(
        shipments_df=shipments_df,
        shipments_containers_df=shipments_containers_df,
        propositions_containers_df=propositions_containers_df,
    )
    shipments_df = shipments_df.sort_values(by=["teus", "tc"], ascending=False)
    shipments_df = shipments_df[
        (~shipments_df.duplicated(subset=[drop_duplicate_key])) | (shipments_df[drop_duplicate_key].isnull())
    ]  # drop duplicates without dropping nan
    return shipments_df
