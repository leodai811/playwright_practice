import pytest
from playwright.sync_api import Page, expect
from typing import List
import time

def click_element(page: Page, selector: str):
    try:
        page.wait_for_selector(selector, state="visible", timeout=10000)
        page.click(selector)
        print(f"✅ 點擊成功: {selector}")
        return True
    except Exception as e:
        print(f"❌ 無法點擊元素 {selector}: {e}")
        return False

def enter_text(page: Page, selector: str, text: str):
    try:
        page.wait_for_selector(selector, state="attached", timeout=10000)
        page.fill(selector, text)
        print(f"✅ 輸入成功: {text} -> {selector}")
        return True
    except Exception as e:
        print(f"❌ 無法輸入 {text} 到 {selector}: {e}")
        return False

def verify_member_id(page: Page, expected_id: str):
    try:
        page.wait_for_selector("#member_no", timeout=10000)
        member_no = page.input_value("#member_no")
        if member_no == expected_id:
            print("✅ PASS: 會員代號正確！")
        else:
            print(f"❌ FAIL: 會員代號錯誤，取得的值為 {member_no}")
    except Exception as e:
        print("❌ 會員代號欄位未找到，測試失敗！", e)


def verify_warranty_device(page: Page, expected_serial_list: List[str]):
    try:
        page.wait_for_selector("a[href='/member/warranty']", timeout=10000)
        page.click("a[href='/member/warranty']")
        page.wait_for_timeout(1000)  # 等待頁面切換完成

        content = page.content()

        for serial in expected_serial_list:
            assert serial in content, f"❌ 找不到保固設備序號 {serial}"
            print(f"✅ PASS: 找到保固設備序號 {serial}")

    except Exception as e:
        print("❌ 保固資訊檢查失敗：", e)
        raise e

@pytest.mark.login
@pytest.mark.parametrize("email, password, expected_id", [
    ("leo.dai@idrip.coffee", "000000", "082801157636")
])
def test_idrip_login(context, email, password, expected_id):
    page = context.new_page()
    page.goto("https://www.idrip.coffee/")

    assert click_element(page, ".siteHeaderAccount")
    assert enter_text(page, "input[type='email']", email)
    assert enter_text(page, "input[type='password']", password)
    assert click_element(page, "input[type='submit']")

    verify_member_id(page, expected_id)

    context.close()

@pytest.mark.warranty
@pytest.mark.parametrize("email, password, expected_serial_list", [
    ("leo.dai@idrip.coffee", "000000", ["IDE1011T000044","IDE1011T0000286","IDE1011T0000928","IDE1011J9999003"])
])
def test_warranty_device(context, email, password, expected_serial_list):
    page = context.new_page()
    page.goto("https://www.idrip.coffee/")

    assert click_element(page, ".siteHeaderAccount")
    assert enter_text(page, "input[type='email']", email)
    assert enter_text(page, "input[type='password']", password)
    assert click_element(page, "input[type='submit']")

    verify_warranty_device(page, expected_serial_list)

    context.close()
