from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Actions
import Logging, time


def auto_declare() -> None:
    page = None
    logging = Logging.Logging()
    sDate = time.strftime("%Y-%m-%d", time.localtime())
    logger = logging.get_log('D:\\log\\' + sDate + 'sasPassportDri.log')
    try:
        logger.info('程序启动')
        path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # 请改为你电脑内Chrome可执行文件路径
        co = ChromiumOptions().set_browser_path(path)
        page = ChromiumPage(co)
        page.get('https://ha.singlewindow.cn/hnsw/swProxy/deskserver/sw/deskIndex?menu_id=sas')
        page.wait.load_start()

        if '修改密码' not in page.html and '海关特殊监管区' not in page.html:
            page.ele('#cardTabBtn').click()
            page.ele("xpath://*[@id='checkboxIntel']").click()
            page.ele('#password').input('66666666')
            page.ele('#loginbutton').click()
            page.wait.load_start()
            page.ele('.layui-layer-btn0').click()
        elif '海关特殊监管区' in page.html:
            pass
        else:
            page.ele('.layui-layer-btn0').click()

        searchElement = page.ele("xpath://*[@id='menu_li']/ul/li[15]/a/span[1]")
        searchElement.click()
        two_steps_declare(page, logger)
        page.refresh()
        searchElement = page.ele("xpath://*[@id='menu_li']/ul/li[15]/a/span[1]")
        searchElement.click()
        custom_declare(page, logger)
    except Exception as e:
        logger.error('主程序异常:' + str(e))
    finally:
        logger.info('程序结束')
        if page is not None:
            page.quit()


# 非两步申报核放单
def custom_declare(page, logger) -> None:
    try:
        page.ele("xpath://*[@id='menu_li']/ul/li[15]/ul/li[9]/a").click()
        page.wait.load_start()
        page.ele('#statusName').input('0')
        ac = Actions(page)
        ac.move_to("@data-value=0").click()
        corps = ['4101630001', '410166A009', '4101660002', '4101661002', '4101660020', '4101662001']
        for corpCode in corps:
            page.ele('#selTradeCode').input(corpCode)
            print(corpCode)
            ac = Actions(page)
            ac.move_to("@data-value=" + corpCode).click()
            cus_declare_recursion(page, logger)
        page.ele("xpath://*[@id='page-wrapper']/div[1]/nav/div/a[2]/i").click()
    except Exception as e:
        logger.error('非两步申报核放单申报失败:' + str(e))


def cus_declare_recursion(page, logger) -> None:
    page.ele("#btn-search").click()
    no_data_btn = page.ele('.layui-layer-btn0')
    page.wait(1)
    if no_data_btn:
        no_data_btn.click()
    else:
        check_boxs = page.eles("@name=btSelectItem")
        tr = page.ele("@data-index=0").text
        seqNo = tr.split('\t')[1].strip()

        if check_boxs:
            check_boxs[0].click()
            page.ele("xpath://*[@id='btn-modify']").click()
            page.wait.load_start()
            declare_btn = page.ele("xpath://*[@id='declearBtn']")
            if declare_btn:
                declare_btn.click()
                page.ele('.layui-layer-btn0').click()
                page.wait(4)
                # 核放单明细页签关闭
                close_btn = "xpath://*[@id='passport-modify-" + seqNo + "']/i"
                page.ele(close_btn).click()
                # page.ele("xpath://*[@id='page-wrapper']/div[1]/nav/div/a[2]").click()
                logger.info("非两步核放单申报成功")
                cus_declare_recursion(page, logger)


# 两步申报
def two_steps_declare(page, logger) -> None:
    try:
        page.ele("xpath://*[@id='menu_li']/ul/li[15]/ul/li[14]/a").click()
        page.wait.load_start()
        page.ele('#statusName').input('0')
        ac = Actions(page)
        ac.move_to("@data-value=0").click()
        two_steps_recursion(page, logger)
    except Exception as e:
        logger.error('两步申报核放单申报失败:' + str(e))


def two_steps_recursion(page, logger):
    page.ele("#btn-search").click()
    no_data_btn = page.ele('.layui-layer-btn0')
    if no_data_btn:
        no_data_btn.click()
    else:
        check_boxs = page.eles("xpath://input[@type='checkbox']")
        if len(check_boxs) > 2:
            check_boxs[2].click()
            page.ele("xpath://*[@id='btn-update']").click()
            page.wait.load_start()
            declare_btn = page.ele("xpath://*[@id='declearIcpBtn']")
            if declare_btn:
                declare_btn.click()
                confirm_btn = page.ele('.layui-layer-btn0')
                if confirm_btn:
                    confirm_btn.click()
                    page.wait(4)
                    logger.info("两步申报核放单申报成功")
                    page.ele("xpath://*[@id='page-wrapper']/div[1]/nav/div/a[3]/i").click()
                    # page.ele("xpath://*[@id='page-wrapper']/div[1]/nav/div/a[2]").click()
                    two_steps_recursion(page, logger)
                else:
                    page.ele("xpath://*[@id='page-wrapper']/div[1]/nav/div/a[3]/i").click()
                    two_steps_recursion(page, logger)
        else:
            page.ele("xpath://*[@id='page-wrapper']/div[1]/nav/div/a[2]/i").click()


if __name__ == '__main__':
    auto_declare()
