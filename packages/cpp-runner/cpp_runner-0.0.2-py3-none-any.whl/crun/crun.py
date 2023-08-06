import os
import argparse


template = """#include <bits/stdc++.h>
using namespace std;
#define read(type) readInt<type>() // Fast read
#define ll long long
#define nL "\\n"
#define pb push_back
#define mk make_pair
#define pii pair<int, int>
#define a first
#define b second
#define vi vector<int>
#define all(x) (x).begin(), (x).end()
#define umap unordered_map
#define uset unordered_set
#define MOD 1000000007
#define imax INT_MAX
#define imin INT_MIN
#define exp 1e9
#define sz(x) (int((x).size()))
int32_t main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int ttt; cin >> ttt;
    while(ttt--) {
    }
    return 0;
}"""


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file to run")
    parser.add_argument("-c", "--create", help="create file",
                        action="store_true")
    args = parser.parse_args()

    if args.create:
        with open(args.filename, "w+") as f:
            f.write(template)
    else:
        os.system(f"g++ {args.filename}")
        os.system(f"./a.out")
        os.system(f"rm -rf ./a.out")


if __name__ == "__main__":
    cli()