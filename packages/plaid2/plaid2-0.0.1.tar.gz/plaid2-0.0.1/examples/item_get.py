from plaid import PlaidClient, AsyncPlaidClient
import asyncio


def main():
    client = PlaidClient.from_env()
    res = client.item_get("access-sandbox-b4957595-eae2-4130-9da7-114d14726a62")
    print(res)


async def async_main():
    client = AsyncPlaidClient.from_env()
    res = await client.item_get("access-sandbox-b4957595-eae2-4130-9da7-114d14726a62")
    print(res)


if __name__ == "__main__":
    main()
    # asyncio.run(async_main())