import sys

from smart_emails import vima_smartcheck

if __name__ == '__main__':
	vima_smartcheck.main(sys.argv[1:])
	sys.exit()
