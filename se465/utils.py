import logging
import os
import subprocess

from django_gitolite.utils import home_dir

logger = logging.getLogger('se465')

def gitolite_creator_call(command):
    try:
        try:
            from subprocess import DEVNULL # py3k
        except ImportError:
            import os
            DEVNULL = open(os.devnull, 'wb')
        subprocess.check_call('ssh git@ecgit.uwaterloo.ca ' + command,
                              shell=True,
                              stdout=DEVNULL,
                              stderr=subprocess.STDOUT,
                              close_fds=True)
    except subprocess.CalledProcessError as e:
        msg = "command '{}' returned {}"
        logger.error(msg.format(e.cmd, e.returncode))

def is_se465_student(username):
    students = ['p23lam', 's78ahmed', 'a4bashir', 'scboyd', 'accendec', 'a77chan', 'kicchan', 'j486chen', 'q48chen', 'q49chen', 'y335chen', 'ypchiu', 'y35cui', 'yx2dai', 'tdhoot', 'zdi', 'z9ding', 'gjgrace', 'c37guo', 'ehauckdo', 'yc2he', 'y49he', 'jhernes', 'hyhu', 'l48huang', 'hjjethwa', 'i3jung', 'd7knight', 'm3knight', 'd76li', 'h248li', 'm92li', 'xy8li', 'z279li', 'jrluo', 'n4ma', 'rdmacken', 'cemoroz', 'gmutter', 'x4ning', 'j58park', 'a3poon', 'erahman', 'fjgroger', 'tshan', 't28shen', 'ksito', 'kjspivak', 'mptatloc', 'sthevara', 'kntinsle', 'atctran', 'd4truong', 'amvaartj', 'c278wang', 'j469wang', 'mq2wang', 'ghwu', 'y33xiao', 'h2xue', 'z9xue', 'b6yan', 'm6ye', 'scye', 'c45yu', 'gjyuan', 'cy2zhang', 'r58zhang', 'm8zheng', 'sjzhu', 'l4zou', 'sreleti', 'x39gao', 'j29peng', 'm32rober', 'y2257wan', 'nababtei', 'mmaltekr', 'salmisha', 'asbhatla', 'slburean', 'x26cao', 'a35chaud', 'x389chen', 'p6cheng', 'l27chu', 'jberbrec', 'sgodavar', 'h3gondal', 'l22gu', 'm34guo', 'dholmesm', 't58huang', 'hjayaram', 'f4jin', 'akaraki', 'maa2khan', 'j538li', 'h268liu', 'w23liu', 'z269liu', 'g7lu', 'smatinkh', 'fmazahir', 'nmedghal', 'mmoodi', 'nnasreen', 'bnithian', 'ypapudes', 'b25peng', 'ppourali', 'z9qiu', 'jk2randh', 'r5rehman', 'j25ross', 'shseifha', 'ptayal', 'd228wang', 'x569wang', 'y2235wan', 'h98wu', 'p5xiao', 'a6yao', 'hyounes', 'l362zhan', 'h82zhu', 's46ahmad', 'h37ahmed', 'aaldhala', 'hjarmstr', 'tbabaran', 'sbalani', 'kj2benne', 'vbollu', 'laburke', 'ajcagala', 'dpmcardo', 'kcarruth', 'yf8chen', 'schiang', 'ischoo', 'bphchow', 'rschuram', 'kwdai', 'jy2deng', 'rmdicecc', 'jgdippel', 'q7dong', 'cfair', 'z5feng', 'cgada', 'ggaisano', 'ewgao', 'alsgaw', 'a3gnanac', 'ja4green', 'tgugoiu', 'mrqhuq', 'lajaneck', 'k2jeong', 'vwjeung', 'nyjiang', 'r22jiang', 'd9jin', 'blajohan', 'ehjung', 's4kabir', 'ckankari', 'askashya', 'ma69khan', 'bj6kim', 'ndklasse', 'ppkwok', 'ja6lee', 'y49lee', 'o3leung', 'jsdli', 's22li', 'kheliao', 'czylin', 'zy4lin', 'xcliu', 'mhlu', 'lhluo', 'mjlyons', 'jmmak', 'rcmak', 'ke2mcbri', 'srmccono', 'simcdona', 'hwmeng', 'l9meng', 'jmizzoni', 'a2mortaz', 'fanaqi', 'jnetterf', 'mnoukhov', 'kokal', 'ooolagok', 'tophelde', 'jtotto', 'xkpan', 'a2pathak', 'eljpembe', 'kapiyara', 'msprysia', 'fjaqures', 'j5rogers', 'msrose', 'phroth', 'amsardes', 'rdsarvar', 'cmschnei', 'h3shao', 'jsshao', 'apsils', 'msindwan', 'psocha', 'vstanche', 'cwstegel', 'lsterick', 'mwstobo', 'd8tang', 'y66tang', 'jetauro', 't7tong', 'mtrivedi', 'httruong', 'z3tu', 'svaithia', 'bjvanryn', 'hmwang', 'r86wang', 'sbwang', 'yt4wang', 'yc8wang', 'd4wei', 'asweinga', 'skcbwen', 'ps2white', 'fwilliam', 'jwirth', 'awiskar', 'lwojciec', 'mmcwong', 'd3woo', 'wtxu', 'hb2yang', 'eyehuda', 'ayiu', 's4yogana', 'z259zhan', 'z63zhao', 'thzhu', 'jlabraha', 'mtaitken', 'aaminpou', 'tcandre', 'hbabaran', 'kbbayrak', 'mtrberzi', 'ascai', 'dcardoso', 'dlwcarr', 'd35chan', 's44chan', 'yknchan', 'mqchen', 'chkchung', 'dcollier', 'sakcraig', 'jfcristi', 'kt2davie', 'apdawide', 'sdermott', 'ardobrik', 'jjfang', 'c8gao', 'jgatt', 'ccgeller', 'sgilcast', 'd4guo', 'jhaider', 'z23he', 'a6hossai', 'a3howe', 'lbhu', 'a26jain', 'gskalsi', 'akaushik', 'ms22khan', 'hj27kim', 'n24kim', 'ayklen', 'alaviole', 'aj5lee', 'ej24lee', 'qfliu', 's3locke', 'e3lou', 'h24lu', 'mcmaclea', 'amaguire', 's7mahara', 'bamcdole', 'smenakur', 'alpang', 'rpeng', 'ja3phill', 'apourhaj', 'jc2price', 'mrabiciu', 'r2ravint', 'mjroukem', 's2saba', 'asaidmur', 's3sathiy', 'nsemenen', 'a46shah', 'ssshan', 'n46sharm', 's7shi', 'spsiddhp', 'd34smith', 'swsomerv', 'yksong', 'asreeniv', 'ajsridha', 'gcbsumid', 'y74sun', 'nsuresh', 'a3swanso', 'e5tam', 'jvong', 'j2vulic', 'ds2wang', 'j332wang', 'm65wang', 'r59wang', 'z286wang', 'a3watson', 'j25wei', 'mwignara', 'm36yang', 't43yu', 'xcyu', 'z3zahid', 'ty4zhang', 'r28zhao', 'hwzhu', 'falmusha', 'jkbaechl', 'dwbinnie', 'jsyho', 'rahoque', 'sjhow', 'pdhung', 'c5kang', 'k35kim', 'j286li', 'q35liu', 'saroach', 'aswami', 'lh2tam', 'tttang', 'stariq', 'pwojcik', 'a53ali', 'j45fu', 'ty3kim']
    return username in students
