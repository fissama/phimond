# internal/auction

Auction house — implements spec §36. TBD.

Will host:

* listing creation with starting bid and buyout;
* listing / storage / transaction fees;
* auction buyout / bid locking so concurrent commands cannot duplicate
  the sale (spec §40 calls out transaction/locking explicitly);
* auction item return and currency transfer;
* mail delivery for sold / unsold items (delegating to `internal/mail`).