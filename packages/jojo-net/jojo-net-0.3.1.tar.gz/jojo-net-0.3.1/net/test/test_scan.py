
from net import *
import unittest


class TestStrUtil(unittest.TestCase):

    def test_match(self):
        self.assertEqual(StrUtil.match(None, None), True)
        self.assertEqual(StrUtil.match(None, '='), False)
        self.assertEqual(StrUtil.match('a=b', None), True)
        self.assertEqual(StrUtil.match('a=b', '='), True)
        self.assertEqual(StrUtil.match('a<b', '='), False)
        self.assertEqual(StrUtil.match('a<b', ('=', '<')), True)
        self.assertEqual(StrUtil.match('<b', ('=', '<')), True)
        self.assertEqual(StrUtil.match('ab', ('=', '<')), False)
        self.assertEqual(StrUtil.match('a<=b', ['<', '=']), True)
        self.assertEqual(StrUtil.match('a=b', ['=', '<']), False)

    def test_split(self):
        self.assertEqual(StrUtil.split(None, None), [])
        self.assertEqual(StrUtil.split("a=b", None), ["a=b"])
        self.assertEqual(StrUtil.split("a=b", "="), ["a", "b"])
        self.assertEqual(StrUtil.split("a b"), ["a", "b"])
        self.assertEqual(StrUtil.split("a  \t b"), ["a", "b"])
        self.assertEqual(StrUtil.split("  a   \tb  c  "), ["a", "b", "c"])
        self.assertEqual(StrUtil.split("  a, b, c", [',', ' ']), ["a", "b", "c"])

    def test_split2(self):
        self.assertEqual(StrUtil.split2(None, None), ('', ''))
        self.assertEqual(StrUtil.split2('a=b', None), ('a=b', ''))
        self.assertEqual(StrUtil.split2('a=b', '='), ('a', 'b'))
        self.assertEqual(StrUtil.split2('a = b', '='), ('a', 'b'))
        self.assertEqual(StrUtil.split2('a < b', ['=', '<']), ('a', 'b'))
        self.assertEqual(StrUtil.split2('ab', '='), ('ab', ''))
        self.assertEqual(StrUtil.split2('ab', '=', first=False), ('', 'ab'))

    def test_split_number_unit(self):
        self.assertEqual(StrUtil.split_number_unit(None), ('', ''))
        self.assertEqual(StrUtil.split_number_unit('33'), (33, ''))
        self.assertEqual(StrUtil.split_number_unit('-8'), (-8, ''))
        self.assertEqual(StrUtil.split_number_unit('-.33'), (-0.33, ''))
        self.assertEqual(StrUtil.split_number_unit('.33'), (0.33, ''))
        self.assertEqual(StrUtil.split_number_unit('23.5'), (23.5, ''))
        self.assertEqual(StrUtil.split_number_unit('33cm'), (33, 'cm'))
        self.assertEqual(StrUtil.split_number_unit('-8cm'), (-8, 'cm'))
        self.assertEqual(StrUtil.split_number_unit('-.33 cm '), (-0.33, 'cm'))
        self.assertEqual(StrUtil.split_number_unit('.33cm'), (0.33, 'cm'))
        self.assertEqual(StrUtil.split_number_unit('23.5cm'), (23.5, 'cm'))

    def test_grep(self):
        line1 = 'Hello, world 888'
        line2 = ' data=5cm, time=33ms'
        line3 = ' data=6cm, time=65ms'
        line4 = ' data=8cm, time=88ms'
        text = line1 + '\n' + line2 + '\n' + line3 + '\n' + line4
        self.assertEqual(StrUtil.grep(None, None), [])
        self.assertEqual(StrUtil.grep(None, '88ms'), [])
        self.assertEqual(StrUtil.grep(text, '888'), [line1])
        self.assertEqual(StrUtil.grep(text, 'data'), [line2, line3, line4])
        self.assertEqual(StrUtil.grep(text, '88ms'), [line4])
        self.assertEqual(StrUtil.grep(text, 'not-exists'), [])
        self.assertEqual(StrUtil.grep(StrUtil.grep(text, 'data'), '33'), [line2])

    def test_is_ip_number(self):
        self.assertEqual(StrUtil.is_ip_number(None), False)
        self.assertEqual(StrUtil.is_ip_number(''), False)
        self.assertEqual(StrUtil.is_ip_number('0'), True)
        self.assertEqual(StrUtil.is_ip_number('255'), True)
        self.assertEqual(StrUtil.is_ip_number('-3'), False)
        self.assertEqual(StrUtil.is_ip_number('888'), False)
        self.assertEqual(StrUtil.is_ip_number(0), True)
        self.assertEqual(StrUtil.is_ip_number(255), True)
        self.assertEqual(StrUtil.is_ip_number(-3), False)
        self.assertEqual(StrUtil.is_ip_number(3.3), False)
        self.assertEqual(StrUtil.is_ip_number(888), False)


class TestNetwork(unittest.TestCase):

    def test_is_ip(self):
        self.assertEqual(Net.is_ip(None), False)
        self.assertEqual(Net.is_ip(''), False)
        self.assertEqual(Net.is_ip('127.0.0.1'), True)
        self.assertEqual(Net.is_ip('abc'), False)
        self.assertEqual(Net.is_ip('127.0.0'), False)
        self.assertEqual(Net.is_ip('127.0.0.258'), False)
        self.assertEqual(Net.is_ip('-27.0.0.1'), False)

    def test_ip_get_set(self):
        self.assertEqual(Net.ip_get('127.0.0.1', 0), 127)
        self.assertEqual(Net.ip_get('127.0.0.1', 3), 1)
        self.assertRaises(TypeError, lambda: Net.ip_get(None, 3))
        self.assertRaises(ValueError, lambda: Net.ip_get('127.0', 3))
        self.assertRaises(ValueError, lambda: Net.ip_get('127.0.0.1', 4))

        self.assertEqual(Net.ip_get(Net.ip_set('127.0.0.1', 0, 188), 0), 188)
        self.assertEqual(Net.ip_get(Net.ip_set('127.0.0.1', 3, 254), 3), 254)
        self.assertRaises(ValueError, lambda: Net.ip_set('127.0', 3, 55))
        self.assertRaises(ValueError, lambda: Net.ip_set('127.0.0.1', 4, 55))

    def test_port_range(self):
        self.assertEqual(len(Net.port_range(10, 10)), 1)
        self.assertEqual(len(Net.port_range(10, 12)), 3)
        self.assertEqual(len(Net.port_range(12, 10)), 3)
        self.assertEqual(13 in Net.port_range(12, 10), False)
        self.assertEqual(10 in Net.port_range(12, 10), True)
        self.assertRaises(ValueError, lambda: Net.port_range(None, 3))
        self.assertRaises(ValueError, lambda: Net.port_range(-3, 3))
        self.assertRaises(ValueError, lambda: Net.port_range(0, 65536))

        self.assertEqual(len(Net.port_range("10-12")), 3)
        self.assertEqual(len(Net.port_range("10,12")), 2)

    def test_ip_range(self):
        self.assertEqual(len(Net.ip_range("192.168.0.1", 1, 10)), 10)
        self.assertEqual("192.168.0.1" in Net.ip_range("192.168.0.1", 1, 10), True)
        self.assertEqual("192.168.0.3" in Net.ip_range("192.168.0.1", 1, 10), True)
        self.assertEqual("192.168.0.10" in Net.ip_range("192.168.0.1", 1, 10), True)
        self.assertEqual("192.168.0.0" in Net.ip_range("192.168.0.1", 1, 10), False)
        self.assertEqual("192.168.0.11" in Net.ip_range("192.168.0.1", 1, 10), False)

        self.assertRaises(TypeError, lambda: Net.ip_range("192.aab.0.1", 1, 10))
        self.assertRaises(ValueError, lambda: Net.ip_range("192.168.0.1", 1, 1880))
        self.assertRaises(ValueError, lambda: Net.ip_range("192.168.0.1", -1, 80))

        self.assertEqual(len(Net.ip_range("192.168.0.*")), 255)
        self.assertEqual(len(Net.ip_range("192.168.0.1-10")), 10)

    def test_local_ip(self):
        self.assertEqual(Net.is_ip(Net.local_ip()), True)

    def test_ping(self):
        ip = Net.local_ip()
        self.assertEqual(Net.ping(ip) >= 0, True)

        mac = Net.get_mac(Net.ip_set(ip, 3, 1))
        # self.assertEqual(len(get_mac(Net.ip_set(ip, 3, 1))) > 0, True)

        ips1 = Net.ip_range(ip, 1, 255)
        result = Net.ip_scan(ips1, mac=3)
        self.assertEqual(len(result) > 0, True)
        ret = [str(item) for item in result]
        print('\n'.join(ret))

        # result = ip_scan(ips1, mac=True)
        # self.assertEqual(len(result) > 0, True)
        # print(result)
        # ips1 = Net.ip_range(ip, 1, 255)
        # result = ip_scan(ips1, mac=2)
        # # print(result)
        # # result = [('a', 'aa'), ('b', 'bb')]
        # ret = [str(item) for item in result]
        # print('\n'.join(ret))


if __name__ == '__main__':
    unittest.main()
