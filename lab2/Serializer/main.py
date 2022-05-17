import math
from serializers.create_serializer import create_serializer

my_dict = {
    "qwe": 123,
    "qwe1": 123124,
    "123": "q23124"
}

class a:
    qwe = 234

    def _show(self):
        return self.qwe + 2042

c = 42
def f(x):
    a = 123
    return math.sin(x * a * c)

def main():
    mytoml = create_serializer("toml")
    myyaml = create_serializer("yaml")
    myjson = create_serializer("json")
    with open("/Users/katasorokina/PycharmProjects/ISP_4sem/lab2/data.toml", "w") as file:
        file.write(mytoml.dumps(f))
        file.close()
    print(mytoml.load("/Users/katasorokina/PycharmProjects/ISP_4sem/lab2/data.toml")(1))

    #myyaml.dump(a, "/Users/katasorokina/PycharmProjects/ISP_4sem/lab2/data.yaml")
    #serclass = myyaml.load("/Users/katasorokina/PycharmProjects/ISP_4sem/lab2/data.yaml")
    #print(serclass.qwe)
    #print(serclass._show(serclass))

    myjson.dump(my_dict, "/Users/katasorokina/PycharmProjects/ISP_4sem/lab2/data.json")
    print(myjson.load("/Users/katasorokina/PycharmProjects/ISP_4sem/lab2/data.json"))


if __name__ == "__main__":
    main()
