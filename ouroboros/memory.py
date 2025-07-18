#!/usr/bin/env python3

from typing import Dict, List, Tuple, Optional, Any
from .errors import RuntimeError

class MemoryBlock:
    """メモリブロックを表現するクラス"""
    def __init__(self, address: int, size: int, data: List[Any] = None):
        self.address = address
        self.size = size
        self.data = data if data is not None else [0] * size
        self.allocated = True
    
    def __repr__(self):
        return f"MemoryBlock(addr=0x{self.address:x}, size={self.size}, allocated={self.allocated})"

class MemoryManager:
    """メモリ管理システム"""
    
    def __init__(self):
        self.heap: Dict[int, MemoryBlock] = {}  # address -> MemoryBlock
        self.next_address = 0x1000  # ヒープの開始アドレス
        self.free_blocks: List[Tuple[int, int]] = []  # (address, size) のフリーブロック
        self.total_allocated = 0
        self.allocation_count = 0
    
    def malloc(self, size: int) -> int:
        """メモリを確保し、アドレスを返す"""
        if size <= 0:
            raise RuntimeError("malloc: Invalid size")
        
        # フリーブロックから適切なサイズを探す
        address = self._find_free_block(size)
        if address is None:
            # 新しいブロックを作成
            address = self.next_address
            self.next_address += size
        
        # メモリブロックを作成
        block = MemoryBlock(address, size)
        self.heap[address] = block
        self.total_allocated += size
        self.allocation_count += 1
        
        return address
    
    def free(self, address: int) -> bool:
        """指定されたアドレスのメモリを解放"""
        if address not in self.heap:
            raise RuntimeError(f"free: Invalid address 0x{address:x}")
        
        block = self.heap[address]
        if not block.allocated:
            raise RuntimeError(f"free: Double free detected at 0x{address:x}")
        
        # ブロックを解放済みとしてマーク
        block.allocated = False
        self.total_allocated -= block.size
        
        # フリーブロックリストに追加
        self.free_blocks.append((address, block.size))
        self._coalesce_free_blocks()
        
        return True
    
    def realloc(self, address: int, new_size: int) -> int:
        """メモリブロックのサイズを変更"""
        if new_size <= 0:
            if address != 0:
                self.free(address)
            return 0
        
        if address == 0:
            return self.malloc(new_size)
        
        if address not in self.heap:
            raise RuntimeError(f"realloc: Invalid address 0x{address:x}")
        
        old_block = self.heap[address]
        if not old_block.allocated:
            raise RuntimeError(f"realloc: Address already freed 0x{address:x}")
        
        # 新しいメモリを確保
        new_address = self.malloc(new_size)
        new_block = self.heap[new_address]
        
        # データをコピー（小さい方のサイズまで）
        copy_size = min(old_block.size, new_size)
        new_block.data[:copy_size] = old_block.data[:copy_size]
        
        # 古いメモリを解放
        self.free(address)
        
        return new_address
    
    def read_memory(self, address: int, offset: int = 0) -> Any:
        """指定されたアドレス+オフセットからデータを読み取り"""
        if address not in self.heap:
            raise RuntimeError(f"read_memory: Invalid address 0x{address:x}")
        
        block = self.heap[address]
        if not block.allocated:
            raise RuntimeError(f"read_memory: Reading from freed memory 0x{address:x}")
        
        if offset < 0 or offset >= block.size:
            raise RuntimeError(f"read_memory: Offset {offset} out of bounds for block size {block.size}")
        
        return block.data[offset]
    
    def write_memory(self, address: int, offset: int, value: Any) -> bool:
        """指定されたアドレス+オフセットにデータを書き込み"""
        if address not in self.heap:
            raise RuntimeError(f"write_memory: Invalid address 0x{address:x}")
        
        block = self.heap[address]
        if not block.allocated:
            raise RuntimeError(f"write_memory: Writing to freed memory 0x{address:x}")
        
        if offset < 0 or offset >= block.size:
            raise RuntimeError(f"write_memory: Offset {offset} out of bounds for block size {block.size}")
        
        block.data[offset] = value
        return True
    
    def get_block_size(self, address: int) -> int:
        """指定されたアドレスのブロックサイズを取得"""
        if address not in self.heap:
            raise RuntimeError(f"get_block_size: Invalid address 0x{address:x}")
        
        return self.heap[address].size
    
    def is_valid_address(self, address: int) -> bool:
        """アドレスが有効かチェック"""
        return address in self.heap and self.heap[address].allocated
    
    def get_memory_info(self) -> Dict[str, Any]:
        """メモリ使用状況を取得"""
        free_blocks_size = sum(size for _, size in self.free_blocks)
        allocated_blocks = sum(1 for block in self.heap.values() if block.allocated)
        
        return {
            'total_allocated': self.total_allocated,
            'allocation_count': self.allocation_count,
            'allocated_blocks': allocated_blocks,
            'free_blocks_count': len(self.free_blocks),
            'free_blocks_size': free_blocks_size,
            'heap_size': len(self.heap)
        }
    
    def _find_free_block(self, size: int) -> Optional[int]:
        """指定されたサイズに適合するフリーブロックを探す"""
        for i, (address, block_size) in enumerate(self.free_blocks):
            if block_size >= size:
                # ブロックを使用
                self.free_blocks.pop(i)
                
                # 残りのサイズがある場合は新しいフリーブロックとして追加
                if block_size > size:
                    remaining_address = address + size
                    remaining_size = block_size - size
                    self.free_blocks.append((remaining_address, remaining_size))
                
                return address
        
        return None
    
    def _coalesce_free_blocks(self):
        """連続するフリーブロックを結合"""
        if len(self.free_blocks) <= 1:
            return
        
        # アドレス順にソート
        self.free_blocks.sort(key=lambda x: x[0])
        
        coalesced = []
        current_addr, current_size = self.free_blocks[0]
        
        for addr, size in self.free_blocks[1:]:
            if current_addr + current_size == addr:
                # 連続するブロックを結合
                current_size += size
            else:
                # 現在のブロックを保存し、新しいブロックを開始
                coalesced.append((current_addr, current_size))
                current_addr, current_size = addr, size
        
        # 最後のブロックを追加
        coalesced.append((current_addr, current_size))
        
        self.free_blocks = coalesced
    
    def debug_dump(self) -> str:
        """デバッグ用のメモリダンプ"""
        lines = ["=== Memory Dump ==="]
        lines.append(f"Total allocated: {self.total_allocated} bytes")
        lines.append(f"Allocation count: {self.allocation_count}")
        lines.append(f"Free blocks: {len(self.free_blocks)}")
        
        lines.append("\nAllocated blocks:")
        for address, block in self.heap.items():
            if block.allocated:
                lines.append(f"  0x{address:08x}: {block.size} bytes")
        
        lines.append("\nFree blocks:")
        for address, size in self.free_blocks:
            lines.append(f"  0x{address:08x}: {size} bytes")
        
        return "\n".join(lines)