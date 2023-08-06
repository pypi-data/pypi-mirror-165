from askdata.human2query import smartner
import time

if __name__ == "__main__":

    # Prod
    # token = "Bc-KxkzVj5COPD_rPb0-uup_MrE"
    # datasets = ["619247D0-CD55-40AA-9B76-09A3BA1AC6DB-MYSQL-024cbe97-00a0-46b0-8252-333351238d9a", "619247D0-CD55-40AA-9B76-09A3BA1AC6DB-MYSQL-d8288331-1ae7-45f7-b129-e726c0634b94"]
    # language = "en"
    # env = "prod"

    # Dev
    token = "GHEBS8pA_fdcAlyeY7y9AogudAc"
    datasets = ['d4262ad1-4aa4-4274-acbb-b79842863841-MYSQL-cf6b6ee6-7fcd-4f4a-bc79-4450b2c09376']
    language = "en"
    env = "dev"

    # Usage
    nl = "price"

    start = time.time()
    smartquery_list = smartner(nl=nl, token=token, datasets=datasets, language=language, env=env, use_cache=False,
                               response_type="anonymize")
    end = time.time()
    for sq in smartquery_list:
        print(sq)
        print()

    print("Time: ", end-start, "s")
