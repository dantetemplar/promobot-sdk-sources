from typing import Any, Optional, Callable
import threading
import asyncio
import time
from concurrent.futures import Future
from sdk.errors import CommandTimeout

class Promise:
    def __init__(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        self._future = Future()
        self._is_active = True
        self._throw_error = throw_error
        self._timeout_seconds = timeout_seconds
        self._timeout_time = time.time() + timeout_seconds
        self._feedback_callbacks = []
        self._success_callbacks: list[Callable[[Any], None]] = []
        self._failure_callbacks: list[Callable[[Exception], None]] = []

        # Для асинхронного ожидания
        self._async_event = None
        self._lock = threading.Lock()
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(self.loop)
            except RuntimeError:
                pass
    
    def _emit_feedback(self, feedback):
        for i, cb in enumerate(self._feedback_callbacks):
            try:
                cb(feedback)
            except Exception as e:
                print(f'[Promise] Error in feedback callback #{i+1}: {e}')

    def _check_timeout(self) -> None:
        current_time = time.time()
        print(f"[PROMISE] _check_timeout: current={current_time:.3f}, timeout_time={self._timeout_time:.3f}")
        
        if self._is_active and current_time > self._timeout_time:
            print(f"[PROMISE] Таймаут наступил, вызываем reject...")
            self.reject(CommandTimeout("Promise timed out"))
        else:
            print(f"[PROMISE] Таймаут не наступил")

    def resolve(self, value: Any) -> None:
        import time
        print(f"[PROMISE] resolve() вызван в {time.time()} с value={value}")
        print(f"[PROMISE] is_active перед resolve: {self._is_active}")
        if self._is_active:
            self._is_active = False
            print(f"[PROMISE] Устанавливаем результат в future...")
            self._future.set_result(value)
            print(f"[PROMISE] Результат установлен, уведомляем async waiters...")
            for i, cb in enumerate(self._success_callbacks):
                try:
                    cb(value)
                except Exception as e:
                    print(f'[Promise] Error in success callback #{i+1}: {e}')
            # Уведомляем асинхронные ожидания
            self._notify_async_waiters()
            print(f"[PROMISE] resolve() завершен")
        else:
            print(f"[PROMISE] Promise уже неактивен, resolve игнорируется")

    def reject(self, reason: Any) -> None:
        import time
        print(f"[PROMISE] reject() вызван в {time.time()} с reason={reason}")
        print(f"[PROMISE] is_active перед reject: {self._is_active}")
        if self._is_active:
            self._is_active = False
            if self._throw_error:
                if not isinstance(reason, Exception):
                    reason = Exception(reason)
                print(f"[PROMISE] Устанавливаем исключение в future...")
                self._future.set_exception(reason)
            else:
                print(f"[PROMISE] Устанавливаем результат ошибки в future...")
                self._future.set_result(reason)
            if isinstance(reason, Exception):
                for i, cb in enumerate(self._failure_callbacks):
                    try:
                        cb(reason)
                    except Exception as e:
                        print(f'[Promise] Error in failure callback #{i+1}: {e}')
            print(f"[PROMISE] Уведомляем async waiters...")
            # Уведомляем асинхронные ожидания
            self._notify_async_waiters()
            print(f"[PROMISE] reject() завершен")
        else:
            print(f"[PROMISE] Promise уже неактивен, reject игнорируется")

    def _notify_async_waiters(self):
        """Уведомляем все асинхронные ожидания о готовности результата"""
        with self._lock:
            if self._async_event:
                try:
                    self.loop.call_soon_threadsafe(self._async_event.set)
                except:
                    pass

    def result(self) -> Any:
        import time
        start_time = time.time()
        print(f"[PROMISE] result() - СТАРТ в {start_time}")
        print(f"[PROMISE] Таймаут: {self._timeout_seconds} сек, осталось: {self._timeout_time - start_time:.2f} сек")
        print(f"[PROMISE] is_active: {self._is_active}")
        print(f"[PROMISE] future.done(): {self._future.done()}")
        
        # Проверяем таймаут перед получением результата
        print(f"[PROMISE] Проверка таймаута...")
        self._check_timeout()
        print(f"[PROMISE] Таймаут проверен, is_active: {self._is_active}")
        
        if not self._is_active:
            print(f"[PROMISE] Promise неактивен после проверки таймаута!")
            # Если Promise был деактивирован из-за таймаута, попробуем получить результат
            if self._future.done():
                try:
                    return self._future.result(timeout=0.1)
                except Exception as e:
                    if self._throw_error:
                        raise
                    else:
                        return e
            else:
                error = CommandTimeout("Promise timed out")
                if self._throw_error:
                    raise error
                else:
                    return error
            
        print(f"[PROMISE] Вызов self._future.result()...")
        try:
            remaining_time = max(0.1, self._timeout_time - time.time())
            result = self._future.result(timeout=remaining_time)
            end_time = time.time()
            print(f"[PROMISE] _future.result() завершен за {end_time - start_time:.3f} сек")
            print(f"[PROMISE] Результат: {result}")
            return result
        except (asyncio.TimeoutError, TimeoutError) as e:
            elapsed = time.time() - start_time
            print(f"[PROMISE] _future.result() ОШИБКА за {elapsed:.3f} сек")
            print(f"[PROMISE] Ошибка: {str(e)}")
            print(f"[PROMISE] Тип ошибки: {type(e).__name__}")
            self._is_active = False
            raise CommandTimeout(f"Превышен таймаут {self._timeout_seconds} сек")
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[PROMISE] _future.result() ОШИБКА за {elapsed:.3f} сек")
            print(f"[PROMISE] Ошибка: {str(e)}")
            print(f"[PROMISE] Тип ошибки: {type(e).__name__}")
            raise

    async def async_result(self) -> Any:
        """Полностью переработанный метод для асинхронного ожидания"""
        # Проверяем, не завершена ли операция уже
        if self._future.done():
            try:
                return self._future.result(self._timeout_seconds)
            except Exception as e:
                raise e
        # Создаем Event для ожидания, если его еще нет
        with self._lock:
            if self._async_event is None:
                self._async_event = asyncio.Event()
        # Определяем оставшееся время до таймаута
        remaining = max(0.1, self._timeout_time - time.time())
        # Ждем с таймаутом
        try:
            await asyncio.wait_for(self._async_event.wait(), timeout=remaining)
        except asyncio.TimeoutError:
            self.reject(CommandTimeout("Promise timed out"))
            raise CommandTimeout("Promise timed out")
        # Попытка получить результат (может вызвать исключение)
        try:
            return self._future.result(timeout=0.1)  # Минимальный таймаут
        except Exception as e:
            raise e
    @property
    def is_active(self) -> bool:
        # Проверяем только флаг, не изменяем его здесь
        return self._is_active

    def __await__(self):
        """Поддержка await для Promise"""
        return self.async_result().__await__()

    def add_success_callback(self, callback: Callable[[Any], None]) -> None:
        if not callable(callback):
            raise ValueError("Success callback must be callable")
        if self._future.done() and not self._future.cancelled() and self._future.exception() is None:
            try:
                callback(self._future.result(self._timeout_seconds))
            except Exception as e:
                print(f'[Promise] Error in immediate success callback: {e}')
        else:
            self._success_callbacks.append(callback)

    def add_failure_callback(self, callback: Callable[[Exception], None]) -> None:
        if not callable(callback):
            raise ValueError("Failure callback must be callable")
        if self._future.done() and self._future.exception() is not None:
            try:
                callback(self._future.exception())
            except Exception as e:
                print(f'[Promise] Error in immediate failure callback: {e}')
        else:
            self._failure_callbacks.append(callback)

    def add_feedback_callback(self, callback: Callable[[Any], None]) -> None:
        if not callable(callback):
            raise ValueError("Feedback callback must be callable")
        self._feedback_callbacks.append(callback)